from fastapi import FastAPI

from app.core.config import settings
from app.db.database import Base, engine
from app.db.models import Article
from app.modules.ingestion.router import router as ingestion_router
from app.modules.ai.router import router as ai_router
from app.modules.articles.router import router as articles_router
from app.modules.editions.router import router as editions_router
from app.modules.ranking.router import router as ranking_router
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router)
app.include_router(ai_router)
app.include_router(articles_router)
app.include_router(editions_router)
app.include_router(ranking_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "bugbaar-api",
    }