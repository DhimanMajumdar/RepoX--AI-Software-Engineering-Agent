import sys
from pathlib import Path
from git import Repo

# Ensure backend root is in sys.path for module resolution
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.ingestion.chunker import chunk_file
from app.ingestion.files import get_repository_files


BASE_DIR = Path(__file__).resolve().parents[3]

REPOS_DIR = BASE_DIR / "data" / "repos"


def clone_repository(repo_url: str, repo_name: str) -> Path:
    repo_path = REPOS_DIR / repo_name

    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    if repo_path.exists():
        return repo_path

    Repo.clone_from(repo_url, repo_path)

    return repo_path
    

if __name__ == "__main__":
    path = clone_repository(
        "https://github.com/psf/requests.git",
        "requests"
    )

    files = get_repository_files(path)

    print(f"Found {len(files)} source files")

    first_file = files[0]

    documents = chunk_file(first_file)

    print(f"\nFile: {first_file}")
    print(f"Chunks: {len(documents)}")

    for document in documents[:3]:
        print("\n--- CHUNK ---")
        print(document.page_content[:300])
        print("METADATA:", document.metadata)