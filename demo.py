from resume_parser import parse_resume
from json_to_doc import jsonl_to_es
from index_builder import create_index
from input_cli import interactive_cli

if __name__ == "__main__":
    # Create the index
    create_index(index_name="resume_index")
    
    # Uncomment to parse resumes - This can take a long time so use the provided JSONL in the next step
    # parse_resume(path="resumes/", output="parsed_resumes.jsonl")
    
    # Step 3: Index the JSONL documents into Elasticsearch
    jsonl_to_es(jsonl_path="parser_output.jsonl", index_name="resume_index")

    # Step 4: Run the interactive CLI for querying
    interactive_cli()
