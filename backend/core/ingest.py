import os
import vertexai
from vertexai.preview import rag

# Default Google Cloud Project and Location (Can be set via env variables)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

def ingest_election_docs(data_dir: str):
    """
    Ingests documents from the specified directory into a Vertex AI RAG Corpus.
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    print(f"Creating RAG Corpus in {LOCATION} for project {PROJECT_ID}...")
    corpus = rag.create_corpus(display_name="election-guide-corpus")
    print(f"Corpus created with name: {corpus.name}")
    
    # Save the corpus name for the API to use
    corpus_file_path = os.path.join(os.path.dirname(__file__), "corpus_name.txt")
    with open(corpus_file_path, "w") as f:
        f.write(corpus.name)
        
    print(f"Ingesting files from {data_dir}...")
    # Import files from the local directory
    response = rag.import_files(
        corpus_name=corpus.name,
        paths=[data_dir],
        chunk_size=512,
        chunk_overlap=50,
        max_embedding_requests_per_min=900,
    )
    
    print(f"Ingestion completed. Imported {response.imported_files_count} files.")
    return corpus.name

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(current_dir, "..", "..", "data", "election-docs")
    
    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)
        print(f"Created empty directory at {data_directory}. Add documents before running ingestion.")
    else:
        ingest_election_docs(data_directory)
