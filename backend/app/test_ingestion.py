import sys
from pathlib import Path

# Add backend directory to sys.path for module resolution
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ingestion.github import clone_repository
from app.ingestion.repository import process_repository
from app.embeddings.model import get_embedding_model
from app.vectorstore.qdrant import get_vector_store


if __name__ == "__main__":
    repo_path = clone_repository(
        "https://github.com/psf/requests.git",
        "requests",
    )

    documents = process_repository(repo_path)

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

    print("Documents added to Qdrant successfully.")

    print("Source files processed successfully.")

    print(f"Total chunks: {len(documents)}")

    for document in documents[:5]:
        print("\n--- CHUNK ---")
        print(document.page_content[:300])
        print("METADATA:")
        print(document.metadata)