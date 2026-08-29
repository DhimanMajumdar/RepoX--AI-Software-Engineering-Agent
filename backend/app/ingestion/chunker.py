from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


CODE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".cs": "csharp",
}


def get_language(file_path: Path) -> str:
    return CODE_EXTENSIONS.get(
        file_path.suffix.lower(),
        "unknown",
    )


def chunk_file(file_path: Path) -> list[Document]:
    content = file_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    language = get_language(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )

    chunks = splitter.split_text(content)

    documents = []

    for index, chunk in enumerate(chunks):
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "file_path": str(file_path),
                    "language": language,
                    "chunk_index": index,
                },
            )
        )

    return documents