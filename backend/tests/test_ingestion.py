from types import SimpleNamespace
from unittest.mock import patch

from app.db.models import Article
from app.modules.ingestion.service import ingest_feed


def test_rss_ingestion_deduplicates_articles(db):
    fake_feed = SimpleNamespace(
        feed={
            "title": "Test Feed",
        },
        entries=[
            {
                "title": "AI Article",
                "link": "https://example.com/ai",
                "summary": "AI news summary",
            },
            {
                "title": "Python Article",
                "link": "https://example.com/python",
                "summary": "Python news summary",
            },
        ],
    )

    with patch(
        "app.modules.ingestion.service.feedparser.parse",
        return_value=fake_feed,
    ):
        first_result = ingest_feed(
            "https://example.com/rss",
            db,
        )

        second_result = ingest_feed(
            "https://example.com/rss",
            db,
        )

    assert first_result["fetched"] == 2
    assert first_result["inserted"] == 2
    assert first_result["skipped"] == 0

    assert second_result["fetched"] == 2
    assert second_result["inserted"] == 0
    assert second_result["skipped"] == 2

    assert db.query(Article).count() == 2