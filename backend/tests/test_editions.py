import pytest

from app.db.models import Article, Edition
from app.modules.editions.service import add_article_to_edition
from app.modules.editions.service import publish_edition


def test_only_approved_articles_can_be_added_to_edition(db):
    edition = Edition(
        title="Test Edition",
        description="Test newsletter",
        status="DRAFT",
    )

    article = Article(
        title="Pending Article",
        url="https://example.com/pending",
        source="Test",
        status="PENDING",
    )

    db.add(edition)
    db.add(article)
    db.commit()

    with pytest.raises(ValueError, match="Only approved articles"):
        add_article_to_edition(
            edition_id=edition.id,
            article_id=article.id,
            db=db,
        )


def test_same_article_is_not_added_twice(db):
    edition = Edition(
        title="Test Edition",
        description="Test newsletter",
        status="DRAFT",
    )

    article = Article(
        title="Approved Article",
        url="https://example.com/approved",
        source="Test",
        status="APPROVED",
    )

    db.add(edition)
    db.add(article)
    db.commit()

    first = add_article_to_edition(
        edition_id=edition.id,
        article_id=article.id,
        db=db,
    )

    second = add_article_to_edition(
        edition_id=edition.id,
        article_id=article.id,
        db=db,
    )

    assert first.id == second.id

    assert len(edition.articles) == 1


def test_empty_edition_cannot_be_published(db):
    edition = Edition(
        title="Empty Edition",
        description="Should not publish",
        status="DRAFT",
    )

    db.add(edition)
    db.commit()
    db.refresh(edition)

    with pytest.raises(
        ValueError,
        match="Cannot publish an empty edition",
    ):
        publish_edition(
            edition_id=edition.id,
            db=db,
        )