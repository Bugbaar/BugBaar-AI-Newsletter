import pytest

from app.db.models import Article
from app.modules.articles.service import update_article_status


def test_article_can_be_approved(db):
    article = Article(
        title="Test Article",
        url="https://example.com/test",
        source="Test",
        status="PENDING",
    )

    db.add(article)
    db.commit()
    db.refresh(article)

    result = update_article_status(
        article_id=article.id,
        status="APPROVED",
        db=db,
    )

    assert result.status == "APPROVED"


def test_invalid_article_status_is_rejected(db):
    article = Article(
        title="Test Article",
        url="https://example.com/test2",
        source="Test",
        status="PENDING",
    )

    db.add(article)
    db.commit()
    db.refresh(article)

    with pytest.raises(ValueError):
        update_article_status(
            article_id=article.id,
            status="INVALID_STATUS",
            db=db,
        )