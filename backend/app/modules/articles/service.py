from sqlalchemy.orm import Session

from app.db.models import Article


VALID_STATUSES = {
    "PENDING",
    "PROCESSING",
    "APPROVED",
    "REJECTED",
}


def get_articles(
    db: Session,
    status: str | None = None,
) -> list[Article]:

    query = db.query(Article)

    if status:
        query = query.filter(Article.status == status.upper())

    return (
        query
        .order_by(Article.relevance_score.desc().nullslast())
        .all()
    )


def get_article(
    article_id: int,
    db: Session,
) -> Article | None:

    return (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )


def update_article_status(
    article_id: int,
    status: str,
    db: Session,
) -> Article | None:

    status = status.upper()

    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status: {status}"
        )

    article = get_article(
        article_id=article_id,
        db=db,
    )

    if article is None:
        return None

    article.status = status

    db.commit()
    db.refresh(article)

    return article