import os
import platform
import subprocess
from elasticsearch import Elasticsearch
from query_builder import build_es_query

es = Elasticsearch("http://localhost:9200")

def send_args(degree: str = None, skills: list = None, title: str = None, career_level: str = None, max_results: int = 5) -> dict:
    """Calls the query builder, attaches a max size, and queries the cluster"""
    query = build_es_query(degree, skills, title, career_level)
    query["size"] = max_results
    output = es.search(index="resume_index", body=query)
    return output

def interactive_cli(degree: str = None, skills: list = None, title: str = None, career_level: str = None) -> None:
    """Interactive CLI that has the user fill out a short questionnaire, creates a query, searches ES cluster, and opens PDF resumes of results"""

    print("Respond to each prompt to execute your search query.\nPress <Enter> without input to match all values for that field.\n")

    # Ask for required degree
    degree = input("What degree is required: ") or None

    # Ask for desired skills - Compares on a logical OR basis
    skills = input("What skills are desired (comma-separated): ") or None
    if skills:
        skills = skills.split(",")
        for skill in skills:
            skill = skill.strip()

    # Ask for desired job title
    title = input("What past job title is desired: ") or None

    # Ask for desired career level
    career_level = input("What career level is desired (entry, mid, senior): ") or None
    while career_level not in [None, "entry", "mid", "senior"]:
        print("Invalid career level, please choose entry, mid, senior, or leave blank")
        career_level = input("What career level is desired (entry, mid, senior): ") or None

    # Ask for how many resumes to retrieve
    max_results = 5
    valid_max = False
    while not valid_max:
        max_results = input("How many resumes to retrieve (default 5): ") or 5
        try:
            max_results = int(max_results)
            valid_max = True
        except ValueError:
            print("Invalid input for max results, please enter an integer value or leave blank")

    # Execute query based on user input
    output = send_args(degree, skills, title, career_level, max_results)

    # Display results and ask to open PDFs
    print(f"{output['hits']['total']['value']} results found, choosing top {max_results}:")
    print(f"IDs: {', '.join([hit['_source']['id'] for hit in output['hits']['hits']])}")
    print("Would you like to open the resume PDFs for these applicants? (y/n)")
    choice = input().strip().lower()
    if choice == 'y' or choice == 'yes':
        for hit in output["hits"]["hits"]:
            resume_id = hit["_source"]["id"]
            pdf_path = f"resumes/{resume_id}.pdf"
            user_os = platform.system()

            # Check for existing file and use OS command to open
            if os.path.isfile(pdf_path):
                if user_os == "Windows":
                    os.startfile(pdf_path)
                elif user_os == "Darwin":
                    subprocess.run(["open", pdf_path])
                elif user_os == "Linux":
                    subprocess.run(["xdg-open", pdf_path])
                else:
                    print(f"Unrecognized OS: {user_os}. Open this file manually: {pdf_path}")
            else:
                print(f"PDF for  ID {resume_id} not found at {pdf_path}")
    else:
        print("PDF's not opened, but can be found in the resumes directory.")

if __name__ == "__main__":
    interactive_cli()
