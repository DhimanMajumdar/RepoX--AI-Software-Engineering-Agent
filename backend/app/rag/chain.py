from typing import cast
from langchain_core.prompts import ChatPromptTemplate

from app.llm.groq import get_llm
from app.retrieval.retriever import get_retriever
from app.rag.schema import RepositoryAnswer


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are RepoX, an expert AI software engineering assistant.
Answer the user's question accurately using ONLY the provided repository context.
If the answer cannot be determined from the context, say "I couldn't find enough information in the repository context."
Do not invent code or behavior.

You MUST respond in JSON format with two keys:
1. "answer": Detailed technical answer to the question.
2. "sources": A JSON list of repository file path strings used to construct the answer (e.g. ["requests/api.py", "requests/sessions.py"]).""",
        ),
        (
            "human",
            """Repository context:
{context}

Question:
{question}""",
        ),
    ]
)


def ask_repository(question: str) -> RepositoryAnswer:
    retriever = get_retriever(k=5)

    documents = retriever.invoke(question)

    context = "\n\n---\n\n".join(
        f"File: {doc.metadata.get('file_path', 'Unknown')}\n{doc.page_content}"
        for doc in documents
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(RepositoryAnswer, method="json_mode")

    chain = PROMPT | structured_llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return cast(RepositoryAnswer, response)