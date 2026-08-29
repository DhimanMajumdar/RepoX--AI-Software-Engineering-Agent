import sys

from pathlib import Path

# Add backend directory to sys.path for module resolution
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.retrieval.retriever import get_retriever


if __name__ == "__main__":
    retriever = get_retriever(k=5)

    query = "How does Requests handle HTTP requests?"

    documents = retriever.invoke(query)

    print(f"Retrieved {len(documents)} documents.")

    for index, document in enumerate(documents, start=1):
        print(f"\n--- RESULT {index} ---")

        print("File:")
        print(document.metadata.get("file_path"))

        print("\nLanguage:")
        print(document.metadata.get("language"))

        print("\nChunk:")
        print(document.page_content[:500])