# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


llm=ChatGroq(
    model="groq/compound-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are RepoX, an AI software engineering assistant.

You help developers understand and debug software repositories.
Be precise and technical."""
    ),
    (
        "human",
        "{question}"
    )
])

chain =prompt | llm

response = chain.invoke({
    "question": "What is the difference between REST and GraphQL?"
})

print(response.content)