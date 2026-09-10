import feedparser

from sqlalchemy.orm import Session

from app.db.models import Article


def ingest_feed(feed_url: str, db: Session) -> dict:
    feed = feedparser.parse(feed_url)

    inserted = 0
    skipped = 0

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        url = entry.get("link", "").strip()

        if not title or not url:
            skipped += 1
            continue

        existing_article = (
            db.query(Article)
            .filter(Article.url == url)
            .first()
        )

        if existing_article:
            skipped += 1
            continue

        article = Article(
            title=title,
            url=url,
            source=feed.feed.get("title", feed_url),
            content=entry.get("summary", ""),
            published_at=None,
            status="PENDING",
        )

        db.add(article)
        inserted += 1

    db.commit()

    return {
        "feed_url": feed_url,
        "fetched": len(feed.entries),
        "inserted": inserted,
        "skipped": skipped,
    }