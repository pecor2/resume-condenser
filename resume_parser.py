import json
import os
import datetime
import pdfplumber
import ollama

# Set schema globally as reference for use in multiple functions
GLOBAL_SCHEMA = """{"education": [{"degree": "string","institution": "string","graduation_year": 1234 }],"experience": [{"title": "string","start_date": "string","end_date": "string"}],"skills": ["string", "string"]}"""

def extract_text_from_pdf(file_path):
    """Use pdfplumber to extract text from a PDF file"""

    text = ""

    # Check if PDF exists, if not return empty string
    if os.path.isfile(file_path) and file_path.lower().endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + '\n'

    return text

def text_to_json(text, resume_id):
    """Use Ollama LLM to convert extracted resume text to JSON"""

    # Create prompt using schema and resume text
    prompt = f"""
        You are a resume parser. Extract the following fields from the resume text. 
        Return ONLY valid JSON. Do not add commentary of any kind.
        JSON Schema:
        {GLOBAL_SCHEMA}

        Resume text:
        {text}

        Output must start with '{{' and end with '}}'
    """

    # Get response and validate
    response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
    json_str =response["message"]["content"]
    valid_json = False
    failures = 0

    # Retry if model gived invalid JSON
    while not valid_json:

        # Check if the response if valid JSON
        try:
            data = json.loads(json_str)
            valid_json = True
            failures = 0

        # Prompt for fix if invalid JSON
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            prompt = f"The following JSON is malformed:\n{json_str}\n\nFix it by returning ONLY corrected, valid JSON. Do not add any explanation, text, or commentary. Output must start with '{{' and end with '}}'.\nCorrected JSON:"
            response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
            json_str = response["message"]["content"]
            failures += 1

        # Recursively parse after 3 failures
        # (potential for endless loop, but low chance with fresh parse)
        if failures >= 3:
            print("3 failures, restarting from fresh parse")
            failures = 0
            data = text_to_json(text, resume_id)

    # Attach ID and return data
    data["id"] = resume_id
    return data

def parse_resume(path: str = "resumes/", output: str = "parser_output.jsonl") -> None:
    """Parse PDFs in resumes directory and send output to JSONL"""
    count = 0
    for file in os.listdir(path):

        

        # Log start time
        start = datetime.datetime.now()

        # Check if file is PDF and process it
        if file.endswith(".pdf") and os.path.isfile(os.path.join(path, file)):
            # REMOVE THIS WHEN SUBNITTING
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            #KIHGDKJGDKJDGHKJDG
            print(count)
            count += 1
            if count <= 1640:
                continue
            file_path = os.path.join(path, file)
            text = extract_text_from_pdf(file_path)
            json_str = text_to_json(text, file[:-4])
            print(f"Processed {file}:")
            print(json.dumps(json_str),"\n\n")
            with open(output, "a", encoding="utf-8") as f:
                f.write(json.dumps(json_str) + "\n")
            end = datetime.datetime.now()
            print(f"Time taken: {end - start}\n\n")
    return None

if __name__ == "__main__":
    parse_resume()
