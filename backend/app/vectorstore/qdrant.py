import atexit
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_qdrant import QdrantVectorStore

from app.embeddings.model import get_embedding_model


COLLECTION_NAME = "repo_code"

_client: QdrantClient | None = None


def close_qdrant_client() -> None:
    """Closes the global Qdrant client cleanly before Python process shutdown."""
    global _client
    if _client is not None:
        try:
            _client.close()
        except Exception:
            pass
        _client = None


atexit.register(close_qdrant_client)


def get_vector_store() -> QdrantVectorStore:
    global _client
    if _client is None:
        _client = QdrantClient(path="data/qdrant")

        if not _client.collection_exists(COLLECTION_NAME):
            _client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=384,  # BAAI/bge-small-en-v1.5 vector dimension
                    distance=models.Distance.COSINE,
                ),
            )

    embeddings = get_embedding_model()

    return QdrantVectorStore(
        client=_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )