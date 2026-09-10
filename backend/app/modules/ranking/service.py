from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Article


def calculate_freshness(article: Article) -> float:
    """
    Returns a freshness score from 0 to 100.

    Articles published recently receive a higher score.
    """

    if article.published_at is None:
        return 50.0

    published = article.published_at

    if published.tzinfo is None:
        published = published.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    age_hours = (
        now - published
    ).total_seconds() / 3600

    if age_hours <= 24:
        return 100.0

    if age_hours <= 72:
        return 80.0

    if age_hours <= 168:
        return 60.0

    if age_hours <= 336:
        return 40.0

    return 20.0


def calculate_rank_score(article: Article) -> float:
    relevance = article.relevance_score or 0
    freshness = calculate_freshness(article)

    score = (
        relevance * 0.60
        + freshness * 0.40
    )

    return round(score, 2)

def select_diverse_articles(
    articles: list[Article],
    limit: int = 10,
) -> list[Article]:

    selected: list[Article] = []
    category_counts: dict[str, int] = {}

    for article in articles:
        category = article.category or "Other"

        count = category_counts.get(category, 0)

        # Avoid having too many articles from one category.
        if count >= 3:
            continue

        selected.append(article)

        category_counts[category] = count + 1

        if len(selected) >= limit:
            break

    return selected


def get_ranked_articles(
    db: Session,
    limit: int = 10,
) -> list[Article]:

    articles = (
        db.query(Article)
        .filter(
            Article.status == "APPROVED",
            Article.relevance_score.isnot(None),
        )
        .all()
    )

    ranked = sorted(
        articles,
        key=calculate_rank_score,
        reverse=True,
    )

    return select_diverse_articles(
        ranked,
        limit=limit,
    )

