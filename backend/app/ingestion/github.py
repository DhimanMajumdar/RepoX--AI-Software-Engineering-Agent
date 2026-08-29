from pathlib import Path
from git import Repo


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

    print(f"Repository cloned to: {path}")