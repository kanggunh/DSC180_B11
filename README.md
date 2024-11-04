# Perovskite Solar Cells: Literature Mining Project

## Retrieving the data locally:

(1) To download the data, simply enter the following url to google spreadsheet and download this as 150_Research_paper.csv:

https://docs.google.com/spreadsheets/d/1nqRxqx5By7RB9sd4FP2A8C4HIG8gLmumeVd3iRfyvzo/edit?usp=sharing

(2) Edit the file: __config/data-params.json__ to include the path/location of the downloaded data in the value of the _indir_ key

## Running the project

* To install the dependencies, run the following command from the root directory of the project: `pip install -r requirements.txt`

### Introduction
This project aims to optimize the discovery of small molecules that improve the stability of perovskite solar cells. By leveraging literature mining, graph-based molecular representations, and machine learning models, we seek to identify patterns that lead to successful molecules and generate deeper insights into perovskite solar cell performance. The current methods rely heavily on Edisonian experimentation, which is inefficient. Our goal is to automate and streamline this discovery process using data-driven techniques.

### Objectives
- Database Creation: Build a comprehensive dataset from scientific literature detailing molecules, their interactions with perovskites, and the outcomes (efficiency, stability, etc.).
- Molecular Representation: Use SMILES (Simplified Molecular Input Line Entry System) to represent molecules in a format suitable for machine learning models.
- Literature Mining: Automate data extraction from published research papers using NLP techniques (e.g., SciBERT, scraping tools).
- Model Training: Develop a model that predicts the success of small molecules in improving perovskite solar cell stability and efficiency.

### Project Timeline
- Exploration: Mining relevant papers and journals and then analyzing and summarize the data we have collected so far.
- Literature Mining: Mining relevant papers from databases and journals, and extracting variables like molecule structure, efficiency, stability, and perovskite composition.
- Model Training: Using the database to train a machine learning model that predicts optimal molecules for perovskite solar cells.

### Running the project
- To install the dependencies, run the following command from the root directory of the project: <code>pip install -r requirements.txt</code>
- To use GROBID (accessed in notebooks_for_checkpoint/scraping_texts.ipynb), install [docker](https://docs.docker.com/engine/install/), 
then run the following command to download and run GROBID's image: <code>docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.1</code>. This will initialize GROBID on http://localhost:8070.
