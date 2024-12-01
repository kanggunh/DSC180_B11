from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
from dotenv import load_dotenv
import json
from litellm import completion
import re
import torch

model_name = "llama-3.2-3b-it-Perovskite-PaperExtractor"
model_name = "meta-llama/Llama-3.2-3B-Instruct"
device = "cuda"

model = AutoModelForCausalLM.from_pretrained(model_name, ).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.model_max_length = 60000
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    temperature=0.1,
    device=0
)

PREFIX = """
You are a helpful scientific assistant. Your task is to extract relevant scientific data from the provided text about perovskite solar cells and passivating molecules. If the data is not available in the text, return null for the respective fields. Output the information in JSON format with the following fields:
- `control_pce`: Power conversion efficiency for control perovskite (numeric).
- `control_voc`: Open-circuit voltage for control perovskite (numeric).
- `treated_pce`: Best Power conversion efficiency for treated perovskite (numeric).
- `treated_voc`: Best Open-circuit voltage for treated perovskite (numeric).
- `passivating_molecule`: Name of the champion passivating molecule tested.
- `perovskite_composition`: Chemical formula of the perovskite (string).
- `electron_transport_layer`: Material used as the electron transport layer (string).
- `hole_transport_layer`: Material used as the hole transport layer (string).
- Stability tests: Include any stability tests mentioned. Stability tests can be done in dark storage (ISOS-D), light-soaking (ISOS-L), thermal cycling (ISOS-T), light cycling (ISOS-LC), and solar-thermal cycling (ISOS-LT). If none of these types are tested, do not include a JSON object for them.
Make sure that all numeric variables are proper javascript numbers. If not, return them as a string.
For each test, the value should follow this format:
```json
{
  "test_name": null, (string - make sure this value is only one of the possible values mentioned: ISOS-D, ISOS-L, ISOS-T, ISOS-LC, ISOS-LT)
  "temperature": null (numeric - only return the number in degrees celsius),
  "time": null,
  "humidity": null (string),
  "control_efficiency": null,
  "treatment_efficiency": null
}

The JSON structure must follow this exact format:
{
  "control_pce": null,
  "control_voc": null,
  "treated_pce": null,
  "treated_voc": null,
  "passivating_molecule": null,
  "perovskite_composition": null,
  "electron_transport_layer": null,
  "hole_transport_layer": null,
  "stability_tests": [
    {
      "test_name": null,
      "temperature": null,
      "time": null,
      "humidity": null,
      "control_efficiency": null,
      "treatment_efficiency": null
    },
  ]
}
Be concise and accurate. Include only information explicitly present in the text.
Don't return ranges for any values, as this will cause the JSON to not parse correctly. If a range is presented, return the range as a string. This is any value that has a "-" in it.
Do not include the "%" sign for any value, this will cause the JSON to parse incorrectly. Either do not include it or return a string - specifically for PCE and effiicency variables.
Do not include the degree symbol for any value, this will cause the JSON to parse incorrectly.
**make sure no unparseable JSON is returned as values for any of these properties**
Only return JSON. The text is below:
"""
SUFFIX = """\n\n{sample}\n\n"""
def create_prompt(system, user):
    tokens = tokenizer.encode(user, max_length=25000, truncation=True)
    truncated_user = tokenizer.decode(tokens)
    return [
    {"role": "system", "content": system},
    {"role": "user", "content": truncated_user}, ]

contents = {}

txt_dir = "../../data/txts"
for filename in os.listdir(txt_dir):
    if filename.endswith(".txt") == False:
        continue
    filepath = os.path.join(txt_dir, filename)
    paper_id = os.path.splitext(filename)[0]
    print(paper_id)

    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()
        instruction = create_prompt(PREFIX, text)
        json_string = pipe(instruction, max_new_tokens=1024)[0]["generated_text"][-1]['content']
        json_match = re.search(r"\{.*\}", json_string, re.DOTALL)
        if json_match:
            raw_json = json_match.group(0).strip()
        else:
            print("No JSON found")
            continue
        try:
            parsed_data = json.loads(raw_json)
            contents[paper_id] = parsed_data
        except json.JSONDecodeError as e:
            print("Error creating JSON", e)
            print(raw_json)

json_path = "../../data/finetuned_llama_output.json"
with open(json_path, "w") as file:
    json.dump(contents, file, indent=4)