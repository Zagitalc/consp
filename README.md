# Durham University BSc Computer Science Final Year Project: First Draft  
## Conspiracy Theories: Understanding and Predicting Conspiratorial Content Using NLP


*Early-stage implementation of conspiracy theory detection using NLP*

## Project Overview
This project aims to analyze linguistic patterns in conspiracy theories using Natural Language Processing (NLP). The early-stage implementation utilizes TF-IDF feature extraction and a Random Forest classifier, with a Flask-based API for text classification.

## Key Features in the First Draft:
- Basic **TF-IDF vectorization** for text representation  
- **Random Forest classifier** for conspiracy classification  
- **Flask web application** with simple API endpoints  
- **Sentence-level classification** with keyword extraction (planned feature)  
- **Prototype UI plans** with mockups (future work)

## Flask API Endpoints (First Draft)

### 1️⃣ Text Classification
- **Endpoint:** `/classify`  
- **Method:** POST  
- **Input Format:** JSON with the following fields:
  - `text`: Content to classify
  - `title`: Title of the content
  - `channel_title`: Source channel or platform
  - `tags`: Tags related to the content
  - `description`: Brief description of the content

**Process:**
- TF-IDF vectorization of input fields
- Classification using the **Random Forest** model
- **Returns:** Classification result (`Conspiracy` or `Not`)

### 2️⃣ Sentence-Level Analysis (Planned Feature)
- Tokenizes input into sentences
- Classifies each sentence individually
- Extracts top-ranked keywords contributing to classification

## Setup & Dependencies

**Required Libraries:**
```bash
pip install flask joblib nltk sklearn numpy

To run the server locally, execute:
```bash
python app.py
