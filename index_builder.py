from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def create_index(index_name: str = "resume_index") -> None:
    """Create an ES index with the following Mapping"""
    # Map ID, Education, Experience, and Skills
    mappings = {
        "properties": {
            "id": {"type": "text"},
            "education": {
                "type": "nested",
                "properties": {
                    "degree": {"type": "text"},
                    "institution": {"type": "text"},
                    "graduation_year": {"type": "integer"}
                }
            },
            "experience": {
                "type": "nested",
                "properties": {
                    "title": {"type": "text"},
                    "start_date": {"type": "date", "format": "strict_date_optional_time||yyyy-MM-dd||MM/yyyy||MM/dd/yyyy||yyyy/MM/dd"},
                    "end_date": {"type": "date", "format": "strict_date_optional_time||yyyy-MM-dd||MM/yyyy||MM/dd/yyyy||yyyy/MM/dd"}
                }
            },
            "skills": {"type": "text"},
            "years_experience": {"type": "integer"}
        }
    }

    # Check if index exists before creating
    if not es.indices.exists(index=index_name):
        print("Creating index")
        try:
            es.indices.create(index=index_name, body={"mappings": mappings})
            print(f"Created {index_name}")
        except Exception as e:
            print(f"Failed to create {index_name}\n{e}")
    else:
        print(f"{index_name} already exists")

if __name__ == "__main__":
    create_index()
