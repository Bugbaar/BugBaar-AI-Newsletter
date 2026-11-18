from pydantic import BaseModel, Field


class AIAnalysis(BaseModel):
    category: str = Field(
        description="One of AI, Engineering, Startups, Careers, Open Source, Research, or Other"
    )

    summary: str = Field(
        description="A concise 2-3 sentence summary of the article"
    )

    key_takeaways: list[str] = Field(
        description="Three concise key takeaways from the article"
    )

    relevance_score: float = Field(
        ge=0,
        le=100,
        description="How relevant this article is to BugBaar readers, from 0 to 100"
    )