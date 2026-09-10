from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.articles.schemas import (
    ArticleResponse,
    ArticleStatusUpdate,
)

from app.modules.articles.service import (
    get_article,
    get_articles,
    update_article_status,
)


router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get(
    "",
    response_model=list[ArticleResponse],
)
def list_articles(
    status: str | None = None,
    db: Session = Depends(get_db),
):
    return get_articles(
        db=db,
        status=status,
    )


@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
)
def retrieve_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    article = get_article(
        article_id=article_id,
        db=db,
    )

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article


@router.patch(
    "/{article_id}/status",
    response_model=ArticleResponse,
)
def change_article_status(
    article_id: int,
    request: ArticleStatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        article = update_article_status(
            article_id=article_id,
            status=request.status,
            db=db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article