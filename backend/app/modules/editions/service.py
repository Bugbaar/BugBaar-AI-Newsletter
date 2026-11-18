from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.db.models import Article, Edition, EditionArticle
from app.modules.ranking.service import get_ranked_articles

def create_edition(
    title: str,
    description: str | None,
    db: Session,
) -> Edition:

    edition = Edition(
        title=title,
        description=description,
        status="DRAFT",
    )

    db.add(edition)
    db.commit()
    db.refresh(edition)

    return edition


def get_editions(
    db: Session,
) -> list[Edition]:

    return (
        db.query(Edition)
        .options(
            joinedload(Edition.articles)
            .joinedload(EditionArticle.article)
        )
        .order_by(Edition.created_at.desc())
        .all()
    )


def get_edition(
    edition_id: int,
    db: Session,
) -> Edition | None:

    return (
        db.query(Edition)
        .options(
            joinedload(Edition.articles)
            .joinedload(EditionArticle.article)
        )
        .filter(Edition.id == edition_id)
        .first()
    )


def add_article_to_edition(
    edition_id: int,
    article_id: int,
    db: Session,
) -> EditionArticle | None:

    edition = (
        db.query(Edition)
        .filter(Edition.id == edition_id)
        .first()
    )

    if edition is None:
        return None

    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if article is None:
        return None

    if article.status != "APPROVED":
        raise ValueError(
            "Only approved articles can be added to an edition"
        )

    existing = (
        db.query(EditionArticle)
        .filter(
            EditionArticle.edition_id == edition_id,
            EditionArticle.article_id == article_id,
        )
        .first()
    )

    if existing:
        return existing

    last_article = (
        db.query(EditionArticle)
        .filter(
            EditionArticle.edition_id == edition_id
        )
        .order_by(
            EditionArticle.position.desc()
        )
        .first()
    )

    next_position = (
        last_article.position + 1
        if last_article
        else 1
    )

    edition_article = EditionArticle(
        edition_id=edition_id,
        article_id=article_id,
        position=next_position,
    )

    db.add(edition_article)
    db.commit()
    db.refresh(edition_article)

    return edition_article


def publish_edition(
    edition_id: int,
    db: Session,
) -> Edition | None:

    edition = get_edition(
        edition_id=edition_id,
        db=db,
    )

    if edition is None:
        return None

    if not edition.articles:
        raise ValueError(
            "Cannot publish an empty edition"
        )

    edition.status = "PUBLISHED"
    edition.published_at = datetime.utcnow()

    db.commit()
    db.refresh(edition)

    return edition


def serialize_edition(
    edition: Edition,
) -> dict:

    return {
        "id": edition.id,
        "title": edition.title,
        "description": edition.description,
        "status": edition.status,
        "published_at": edition.published_at,
        "articles": [
            {
                "position": item.position,
                "article_id": item.article_id,
                "title": item.article.title,
                "summary": item.article.summary,
                "category": item.article.category,
                "relevance_score": item.article.relevance_score,
                "url": item.article.url,
            }
            for item in sorted(
                edition.articles,
                key=lambda x: x.position,
            )
        ],
    }


from app.modules.ranking.service import get_ranked_articles


def generate_edition_articles(
    edition_id: int,
    limit: int,
    db: Session,
) -> Edition | None:

    edition = get_edition(
        edition_id=edition_id,
        db=db,
    )

    if edition is None:
        return None

    if edition.status != "DRAFT":
        raise ValueError(
            "Articles can only be generated for a draft edition"
        )

    ranked_articles = get_ranked_articles(
        db=db,
        limit=limit,
    )

    # Existing articles are removed so generation is repeatable.
    for existing in list(edition.articles):
        db.delete(existing)

    db.flush()

    for position, article in enumerate(
        ranked_articles,
        start=1,
    ):
        edition_article = EditionArticle(
            edition_id=edition.id,
            article_id=article.id,
            position=position,
        )

        db.add(edition_article)

    db.commit()
    db.refresh(edition)

    return get_edition(
        edition_id=edition.id,
        db=db,
    )