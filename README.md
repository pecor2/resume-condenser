# Resume Condenser

A project for UIUC CS410

## Description

The Resume Condenser will take a resume (or list of resumes) as input and condense them down into an easily parsable format for a recruiter or hiring manager to analyze the contents. This will allow a stack of resumes to be transformed into a standardized format that can be used to retain and evaluate job applicant resumes.

## Getting Started

Download elasticsearch here: https://www.elastic.co/downloads/elasticsearch

Download Docker Desktop here: https://www.docker.com/products/docker-desktop

Download Ollama here: https://ollama.com/download

Resume PDF dataset in the `resumes` directory provided by Kaggle: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset

### Dependencies

* Python Libraries all included in requirements.txt
* ElasticSearch version 8.0+
* Docker Desktop 
* Ollama llama3.2:3b

### Setup

* Create virtual env and activate
  * `python -m venv venv`
  * `source venv/bin/activate`
* Import requirements
  * `pip install -r requirements.txt`
* Launch Docker, then set up an ES cluster locally at `localhost:9200`:
  * The `start.sh` script in the `elastic-start-local` has been configured to set up a no-auth ES and Kibana cluster.
* Launch Ollama then pull model `llama3.2:3b`:
  * `ollama pull llama3.2:3b`
* (OPTIONAL) Get parsed resumes:
  * Over 1500 pre-parsed resumes are available in `parser_output.jsonl` so this step is optional. 
  * Additional resumes can be added to the `resumes` directory and parsed by running `python resume_parser.py` (Takes a very long time)
* Run `demo.py` to see a demo:
  * First it will try and create an index `resume_index` with proper mappings
  * Next it will load all parsed resumes from `parser_output.jsonl` into ES
  * Finally it will ask a series of questions in the CLI to find applicable resumes
    * After the demo has been run once, you can just re-run the CLI directly with `python imput_cli.py`

### Demo Output 
User input is denoted by surrounding angle brackets `<input>`
```
> python demo.py
Creating index
Created resume_index
Indexing documents from parser_output.jsonl into 'resume_index'
Document ID 30563572: created
Document ID 57364820: created
...
Document ID 26921245: created
Indexing complete: 1466 / 1628 documents indexed.
Respond to each prompt to execute your search query.
Press <Enter> without input to match all values for that field.

What degree is required: <bachelor>
What skills are desired (comma-separated): <office,python,excel>
What past job title is desired: <engineer>
What career level is desired (entry, mid, senior): <mid>
How many resumes to retrieve (default 5): <2>
4 results found, choosing top 2:
IDs: 19396040, 22450718
Would you like to open the resume PDFs for these applicants? (y/n)
<yes>
```
After this, the selected resumes are opened in the default PDF viewer.
