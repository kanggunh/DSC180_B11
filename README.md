# Perovskite Solar Cells: Literature Mining Project

### File Structure
```
DSC180_B11
└───data
│    │   biocs/                                # TeamTat annotations in XML files
│    │   model_results/                        # Classfication Model performance results
│    │   txts/                                 # Raw text files of the 150 articles
│    │   xmls/                                 # XML files of the 150 articles
│    │   150_research_papers.csv               # Dataset of 150 research papers
│    │   bioc_parsed.csv                       # Parsed BIOC data
│    │   good_paper_links.csv                  # Sample Relevant paper links for classification
│    │   irrelevant_papers.csv                 # Sample Irrelevant papers classification
│    │   merged_label.csv                      # Combined labeled dataset for classification task
│    │   model_performance_results.csv         # Performance metrics for models
│    │   Perovskite_database_content_all_data.csv # Database for perovskite solar cells
│    │   text_bad_paper.csv                    # Text from irrelevant papers
│    │   text_good_paper.csv                   # Text from relevant papers
│    └───training_data.csv                     # Dataset for training the models
│
└───images
│    │   classification_compare.png            # Model comparison visualization
│    │   pipeline_flowchart.png                # Workflow diagram
│    └───q2_timeline.png                       # Project timeline visualization
│
└───models
│    │   llama-3.2-3b-it-Perovskite-PaperExtractor/ # Fine-tuned LLaMA model files
│    └───scibert_psc_ner_model/                # SciBERT model files
│
└───q1_submission_notebooks
│    │   01_extract_link_badpaper.py           # Script for extracting bad paper links
│    │   02_Scrapint_texts.ipynb               # Notebook for text scraping
│    │   03_TF-IDF_vectorizer_and_models.ipynb # TF-IDF vectorization and modeling
│    │   04_flan_model.ipynb                   # FLAN-T5 model implementation
│    │   05_sciBERT.ipynb                      # SciBERT model implementation
│    │   06_scraping_and_conversion.ipynb      # Data scraping and format conversion 
│    │   07_llama_training.ipynb               # LLaMA training notebook
│    │   08_finetuned_llama_extraction.ipynb   # LLaMA fine-tuned model extraction
│    │   09_evaluation.ipynb                   # Evaluation of model performance
│    │   10_scibert_training.ipynb             
│    └───11_database_searcher.ipynb            
│
└───README.md                                  # Documentation for the project
└───requirements.txt                           # Python dependencies
└───run.py                                     # Main script for executing the pipeline

```

### Introduction
This project aims to optimize the discovery of small molecule that improve the stability of perovskite solar cells. By leveraging literature mining, graph-based molecular representations, and machine learning models, we seek to identify patterns that lead to successful molecules and generate deeper insights into perovskite solar cell performance. The current methods rely heavily on Edisonian experimentation, which is inefficient. Our goal is to automate and streamline this discovery process using data-driven techniques, focusing on the vast body of research already conducted in this field.

### Objectives
- Collects bodies of research paper links and classify the paper that is relevent to our specific domain or not. 
- Database Creation: Build a comprehensive dataset from scientific literature detailing molecules, their interactions with perovskites, and the outcomes (efficiency, stability, etc.).
- Molecular Representation: Use SMILES (Simplified Molecular Input Line Entry System) to represent molecules in a format suitable for machine learning models.
- Literature Mining: Automate data extraction from published research papers using NLP techniques (e.g., SciBERT, scraping tools).
- Model Training: Develop a model that predicts the success of small molecules in improving perovskite solar cell stability and efficiency.

<img src="images\pipeline_flowchart.png" alt="pipeline" width="1000">


### Project Timeline
- Paper collection / filtering: Develop a classification model that, given a research paper link, determines whether the paper is relevant to our study. Relevant papers are then processed for further data mining.
- Exploration: Mining relevant papers and journals and then analyzing and summarize the data we have collected so far.
- Literature Mining: Mining relevant papers from databases and journals, and extracting variables like molecule structure, efficiency, stability, and perovskite composition.
- Model Training: Using the database to train a machine learning model that predicts optimal molecules for perovskite solar cells.

## Retrieving the data locally:

(1) To download the data, simply enter the following url to google spreadsheet and download this as 150_Research_paper.csv:

https://docs.google.com/spreadsheets/d/1nqRxqx5By7RB9sd4FP2A8C4HIG8gLmumeVd3iRfyvzo/edit?usp=sharing

(2) Edit the file: __config/data-params.json__ to include the path/location of the downloaded data in the value of the _indir_ key

## Running the project

- To install the dependencies, run the following command from the root directory of the project: <code>pip install -r requirements.txt</code>
- To use GROBID (accessed in notebooks_for_checkpoint/xml_generator.ipynb), install [docker](https://docs.docker.com/engine/install/), 
then run the following command to download and run GROBID's image: <code>docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.1</code>. This will initialize GROBID on http://localhost:8070.


## General Guidelines and Explanation of Our Work
All relevant files for evaluation are located in the `notebooks_for_checkpoint` folder. Below is the recommended order for running these files.

### Step 1: Generating a Relevant vs. Irrelevant Research Papers Database for Classification

1. **`1_extract_link_badpaper.py`**  
   This script takes two URLs of irrelevant research papers, performs literature mining, and scrapes all references from these papers. These references form a training set representing irrelevant papers.  
   - **Output**: After successful execution, it generates an `irrelevant_papers.csv` file in the `data` folder.

2. **`2_Scrapint_texts.ipynb`**  
   Ensure that two CSV files, `150_research_papers.csv` and `irrelevant_papers.csv`, are available in the `data` folder. This notebook accesses these research papers via URLs and extracts clean text data.  
   - **Output**: Upon completion, it outputs a `merged_label.csv` file in the `data` folder, which is used for classification testing.

### Step 2: Building and Evaluating Classification Models

1. **`3_TF-IDF_vectorizer_and_models.ipynb`**  
   This notebook performs five classification algorithms:
   - Logistic Regression
   - Naive Bayes
   - SVM
   - Random Forest
   - XGBoost  

   Each model undergoes hyperparameter tuning to find optimal settings. The results are saved as CSV files in the `data/model_results` folder, and visualizations show the performance before and after tuning.

2. **`4_flan_model.ipynb`**  
   This notebook performs classification using Google’s Fine-tuned Language Net model.  
   - **Output**: The performance results are saved as a CSV file in the `data/model_results` folder.

3. **`5_sciBERT.ipynb`**  
   This notebook performs classification using the SciBERT model.  
   - **Output**: The performance results are saved as a CSV file in the `data/model_results` folder.

4. **`6_model_analysis.ipynb`**  
   This notebook aggregates the results from all models and compares the Accuracy, Recall, and Balanced Error Rate (BER) metrics for each model. Visualizations illustrate these comparisons, showing Random Forest with the highest Accuracy and BER.
   - **Visualization**:  
     <img src="images\classification_compare.png" alt="Comparing performance metric for ALL classification perfomed " width="400">

### Additional Tasks for Data Extraction

1. **`7_database_searcher.ipynb`**  
   This notebook includes a function that retrieves key variables (e.g., efficiency, condition, PCE) from a given research paper's DOI using the Perovskite Database. It is intended for use in the extraction phase of our project.

2. **`8_xml_generator.ipynb`**  
   This notebook generates a PDF version of a research paper from its link and then converts it into XML using GROBID. The generated PDFs and XML files are stored in the `data/pdfs` and `data/xmls` folders, respectively.

