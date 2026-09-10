from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.ingestion.schemas import (
    FeedRequest,
    IngestionResponse,
)
from app.modules.ingestion.service import ingest_feed


router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)


@router.post("/rss", response_model=IngestionResponse)
def ingest_rss(
    request: FeedRequest,
    db: Session = Depends(get_db),
):
    return ingest_feed(
        feed_url=str(request.feed_url),
        db=db,
    )