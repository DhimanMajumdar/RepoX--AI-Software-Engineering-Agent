from typing import AsyncGenerator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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
Do not invent code or behavior.""",
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


async def astream_ask_repository(question: str) -> AsyncGenerator[str, None]:
    retriever = get_retriever(k=5)

    documents = await retriever.ainvoke(question)

    context = "\n\n---\n\n".join(
        f"File: {doc.metadata.get('file_path', 'Unknown')}\n{doc.page_content}"
        for doc in documents
    )

    llm = get_llm()

    chain = PROMPT | llm | StrOutputParser()

    async for chunk in chain.astream(
        {
            "context": context,
            "question": question,
        }
    ):
        yield chunk