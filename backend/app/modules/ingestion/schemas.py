from datetime import datetime

from pydantic import BaseModel, HttpUrl


class FeedRequest(BaseModel):
    feed_url: HttpUrl


class IngestionResponse(BaseModel):
    feed_url: str
    fetched: int
    inserted: int
    skipped: int