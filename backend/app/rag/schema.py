from pydantic import BaseModel, Field


class RepositoryAnswer(BaseModel):
    """Repository Answer"""

    answer: str = Field(description="Answer to the user's question")
    sources: list[str] = Field(
        default_factory=list,
        description="Sources used to generate the answer (repository file paths)",
    )