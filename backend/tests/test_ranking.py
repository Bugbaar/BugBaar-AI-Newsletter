from datetime import datetime, timezone

from app.db.models import Article
from app.modules.ranking.service import (
    calculate_freshness,
    calculate_rank_score,
    select_diverse_articles,
)


def test_rank_score_combines_relevance_and_freshness():
    article = Article(
        title="Important AI News",
        url="https://example.com/1",
        source="Test Source",
        relevance_score=80,
        published_at=datetime.now(timezone.utc),
    )

    score = calculate_rank_score(article)

    assert score == 88.0


def test_category_diversity_limits_articles_per_category():
    articles = []

    for i in range(5):
        articles.append(
            Article(
                title=f"AI Article {i}",
                url=f"https://example.com/ai-{i}",
                source="Test",
                category="AI",
                relevance_score=100 - i,
            )
        )

    for i in range(2):
        articles.append(
            Article(
                title=f"Engineering Article {i}",
                url=f"https://example.com/eng-{i}",
                source="Test",
                category="Engineering",
                relevance_score=90 - i,
            )
        )

    selected = select_diverse_articles(
        articles,
        limit=10,
    )

    ai_count = sum(
        1 for article in selected
        if article.category == "AI"
    )

    assert ai_count <= 3