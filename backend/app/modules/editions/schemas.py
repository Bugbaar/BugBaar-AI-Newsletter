from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EditionCreate(BaseModel):
    title: str
    description: str | None = None


class EditionArticleAdd(BaseModel):
    article_id: int


class EditionArticleResponse(BaseModel):
    position: int
    article_id: int
    title: str
    summary: str | None
    category: str | None
    relevance_score: float | None
    url: str

    model_config = ConfigDict(from_attributes=True)


class EditionResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    published_at: datetime | None
    articles: list[EditionArticleResponse]

    model_config = ConfigDict(from_attributes=True)