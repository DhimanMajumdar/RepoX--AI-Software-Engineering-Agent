from langchain_core.retrievers import BaseRetriever

from app.vectorstore.qdrant import get_vector_store


def get_retriever(k: int = 5) -> BaseRetriever:
    vector_store = get_vector_store()

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
        },
    )