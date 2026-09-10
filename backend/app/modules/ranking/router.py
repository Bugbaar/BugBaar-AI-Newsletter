from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.articles.schemas import ArticleResponse
from app.modules.ranking.service import get_ranked_articles


router = APIRouter(
    prefix="/ranking",
    tags=["Ranking"],
)


@router.get(
    "/articles",
    response_model=list[ArticleResponse],
)
def ranked_articles(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    db: Session = Depends(get_db),
):
    return get_ranked_articles(
        db=db,
        limit=limit,
    )