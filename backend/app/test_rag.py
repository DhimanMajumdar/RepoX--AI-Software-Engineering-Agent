import sys
from pathlib import Path

# Add backend directory to sys.path for module resolution
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag.chain import ask_repository


if __name__ == "__main__":
    question = "How does Requests handle HTTP requests?"
    print(f"Question: {question}\n")
    
    try:    
        response = ask_repository(question)
        print("--- REPOX ANSWER ---")
        print(response.answer)
        print("\n--- SOURCES ---")
        for source in response.sources:
            print("-", source)
    except Exception as e:
        print(f"Error executing RAG chain: {e}")