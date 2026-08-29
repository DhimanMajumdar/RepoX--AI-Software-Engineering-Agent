from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.files import get_repository_files
from app.ingestion.chunker import chunk_file


def process_repository(repo_path: Path) -> list[Document]:
    files = get_repository_files(repo_path)

    documents: list[Document] = []

    for file_path in files:
        file_documents = chunk_file(file_path)
        documents.extend(file_documents)

    return documents