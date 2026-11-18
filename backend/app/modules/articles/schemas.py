from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    source: str
    content: str | None
    summary: str | None
    category: str | None
    key_takeaways: list | None
    relevance_score: float | None
    status: str
    published_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ArticleStatusUpdate(BaseModel):
    status: str