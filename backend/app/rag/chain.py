from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.llm.groq import get_llm
from app.retrieval.retriever import get_retriever


PROMPT = ChatPromptTemplate.from_template(
    """
You are RepoX, an AI assistant that answers questions about GitHub repositories.

Use ONLY the provided repository context to answer the question.

If the answer cannot be determined from the context, say:
"I couldn't find enough information in the repository context."

Do not invent code or behavior.

Repository context:
{context}

Question:
{question}

Answer:
"""
)


def ask_repository(question: str) -> str:
    retriever = get_retriever(k=5)

    documents = retriever.invoke(question)

    context = "\n\n---\n\n".join(
        document.page_content
        for document in documents
    )

    llm = get_llm()

    chain = PROMPT | llm | StrOutputParser()

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return response