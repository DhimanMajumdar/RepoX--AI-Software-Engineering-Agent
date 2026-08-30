import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path for module resolution
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag.chain import astream_ask_repository


async def main():
    question = "How does Requests handle HTTP requests?"
    print(f"Question: {question}\n")
    print("--- REPOX ANSWER STREAM ---")
    
    try:
        async for chunk in astream_ask_repository(question):
            print(chunk, end="", flush=True)
        print()
    except Exception as e:
        print(f"\nError executing RAG chain: {e}")


if __name__ == "__main__":
    asyncio.run(main())