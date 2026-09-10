from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.ai.schemas import AIAnalysis
from app.modules.ai.service import analyze_article_by_id


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/articles/{article_id}/analyze",
    response_model=AIAnalysis,
)
def analyze_article_endpoint(
    article_id: int,
    db: Session = Depends(get_db),
):
    result = analyze_article_by_id(
        article_id=article_id,
        db=db,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return result