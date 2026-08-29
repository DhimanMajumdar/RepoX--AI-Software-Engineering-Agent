from typing import cast
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field

class RepoXResponse(BaseModel):
    answer:str=Field(description="The technical answer to the developer's question")
    key_points:list[str]=Field(description="Important technical points from the answer")
    

load_dotenv()


llm=ChatGroq(
    model="groq/compound-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(RepoXResponse, method="json_mode")

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are RepoX, an AI software engineering assistant.
You help developers understand and debug software repositories.
Be precise and technical.
Respond in valid JSON with keys 'answer' and 'key_points'."""
    ),
    (
        "human",
        "{question}"
    )
])

chain = prompt | structured_llm

response = cast(RepoXResponse, chain.invoke({
    "question": "What is the difference between REST and GraphQL?"
}))

print("Answer:")        
print(response.answer)

print("\nKey Points:")
for point in response.key_points:
    print("-", point)