from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Article
from app.modules.ai.schemas import AIAnalysis


client = genai.Client(
    api_key=settings.gemini_api_key
)


SYSTEM_PROMPT = """
You are the AI editor for BugBaar AI Newsletter.

BugBaar is a technology newsletter covering:

- Artificial Intelligence
- Software Engineering
- Startups
- Careers
- Open Source
- Research

Analyze the provided article.

Your job is to:

1. Select the most appropriate category.
2. Write a concise 2-3 sentence summary.
3. Extract exactly 3 important takeaways.
4. Give the article a relevance score from 0 to 100.

Relevance should consider:
- Technical importance
- Novelty
- Practical usefulness
- Importance to developers/AI engineers/startup builders
- Potential interest to technology readers

Do not invent facts that are not present in the article.
"""


def analyze_article(article: Article) -> AIAnalysis:
    content = article.content or ""

    prompt = f"""
{SYSTEM_PROMPT}

ARTICLE TITLE:
{article.title}

ARTICLE SOURCE:
{article.source}

ARTICLE URL:
{article.url}

ARTICLE CONTENT:
{content}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AIAnalysis,
            temperature=0.2,
        ),
    )

    return AIAnalysis.model_validate_json(response.text)


def analyze_article_by_id(
    article_id: int,
    db: Session,
) -> AIAnalysis | None:

    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if article is None:
        return None

    article.status = "PROCESSING"
    db.commit()

    try:
        analysis = analyze_article(article)

        article.category = analysis.category
        article.summary = analysis.summary
        article.key_takeaways = analysis.key_takeaways
        article.relevance_score = analysis.relevance_score

        article.status = "PENDING"

        db.commit()
        db.refresh(article)

        return analysis

    except Exception:
        article.status = "PENDING"
        db.commit()
        raise