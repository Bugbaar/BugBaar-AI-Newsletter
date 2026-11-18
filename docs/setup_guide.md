# BugBaar AI Newsletter

An AI-powered technology content curation and newsletter platform that collects articles from RSS feeds, analyzes them with Google Gemini, ranks them by relevance and freshness, and lets an editor review and publish curated newsletter editions.

## Overview

BugBaar AI Newsletter automates the repetitive parts of technology content curation while keeping a human editor in control.

### Core workflow

```text
RSS Feeds
   ↓
Article Ingestion
   ↓
Deduplication
   ↓
AI Analysis with Gemini
   ↓
Category + Summary + Key Takeaways + Relevance Score
   ↓
Editor Review
   ↓
Approved Articles
   ↓
Ranking
   ↓
Newsletter Edition
   ↓
Human Review
   ↓
Published Newsletter
```

The system uses RSS summaries/descriptions as the article content source. It intentionally does not scrape full article pages.

## Features

* RSS feed ingestion
* Idempotent article ingestion and URL-based deduplication
* AI-powered article analysis using Google Gemini
* Automatic categorization
* Concise article summaries
* Key takeaway extraction
* Relevance scoring
* Freshness-aware article ranking
* Category diversity during article selection
* Human approval/rejection workflow
* Newsletter edition creation
* Automatic selection of approved articles for an edition
* Public newsletter pages
* PostgreSQL persistence
* REST API with FastAPI
* Next.js frontend
* Docker Compose development/deployment setup
* Pytest test suite
* CORS configuration
* Typed TypeScript API layer

## Tech Stack

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Feedparser
* Google Gemini (`google-genai`)
* Pytest

### Frontend

* Next.js
* TypeScript
* React
* Tailwind CSS

### Infrastructure

* Docker
* Docker Compose
* PostgreSQL

## Architecture

The project follows a modular-monolith architecture.

```text
bugbaar-ai-newsletter/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── models/
│   │   │       ├── article.py
│   │   │       ├── edition.py
│   │   │       └── user.py
│   │   │
│   │   ├── modules/
│   │   │   ├── ingestion/
│   │   │   ├── ai/
│   │   │   ├── articles/
│   │   │   ├── ranking/
│   │   │   ├── editions/
│   │   │   └── auth/
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app/
│   │   ├── articles/
│   │   ├── editions/
│   │   ├── newsletter/
│   │   └── login/
│   │
│   ├── components/
│   ├── lib/
│   ├── types/
│   └── Dockerfile
│
├── docs/
│   └── architecture.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Ranking

Articles are ranked using relevance and freshness:

```text
Final Score =
    Relevance Score × 0.60
    +
    Freshness Score × 0.40
```

The selection logic also limits the number of articles from a single category so that one category does not dominate the newsletter.

## Article Lifecycle

```text
PENDING
   ↓
AI Processing
   ↓
PENDING
   ↓
Editor Review
   ├── APPROVED
   └── REJECTED
```

Only approved articles can be added to a newsletter edition.

## Newsletter Lifecycle

```text
DRAFT
  ↓
Articles Added
  ↓
Editor Review
  ↓
PUBLISHED
```

An empty edition cannot be published.

## Running Locally

### Prerequisites

Install:

* Python 3.12+
* Node.js 20+
* Docker Desktop
* Git
* A Google Gemini API key

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd BugBaar-AI-Newsletter
```

### 2. Configure environment variables

Create a root `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

For local development, configure the backend environment as required by `backend/app/core/config.py`.

Do not commit `.env` or any secret API keys.

## Run with Docker

Build the containers:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

The services are:

| Service    | URL                        |
| ---------- | -------------------------- |
| Frontend   | http://localhost:3000      |
| Backend    | http://localhost:8000      |
| API Docs   | http://localhost:8000/docs |
| PostgreSQL | localhost:5432             |

Check backend health:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "bugbaar-api"
}
```

To stop the services:

```bash
docker compose down
```

## Run Without Docker

### Backend

```bash
cd backend

python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

The frontend API URL can be configured using:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Example RSS Feed

For testing RSS ingestion:

```text
https://hnrss.org/frontpage
```

Example endpoint:

```http
POST /ingestion/rss
```

Request:

```json
{
  "feed_url": "https://hnrss.org/frontpage"
}
```

Running the same feed again will skip articles whose URLs already exist.

## Important API Endpoints

### Health

```http
GET /health
```

### Articles

```http
GET /articles
GET /articles/{article_id}
PATCH /articles/{article_id}/status
```

### AI

```http
POST /ai/articles/{article_id}/analyze
```

### Ingestion

```http
POST /ingestion/rss
```

### Ranking

```http
GET /ranking/articles
```

### Editions

```http
POST /editions
GET /editions
GET /editions/{edition_id}
POST /editions/{edition_id}/articles
PATCH /editions/{edition_id}/publish
```

## Testing

The backend includes a focused Pytest suite covering important business rules.

Run:

```bash
cd backend
pytest -v
```

Current test coverage includes:

* RSS ingestion deduplication
* Ranking score calculation
* Category diversity
* Article approval/rejection validation
* Preventing empty editions from being published
* Preventing unapproved articles from entering editions
* Preventing duplicate articles inside an edition

## Design Decisions

### Why RSS instead of full article scraping?

RSS provides a simple and reliable source for article metadata and summaries without introducing the complexity and legal/technical variability of scraping different websites.

### Why synchronous AI processing?

The assessment focuses on correctness and a clear end-to-end workflow. Synchronous processing keeps the implementation simple while still isolating AI failures from the rest of the ingestion pipeline.

### Why a modular monolith?

A modular monolith provides clear separation of concerns without introducing unnecessary operational complexity such as Kafka, Kubernetes, Redis, or multiple independently deployed services.

### Why human approval?

AI-generated summaries and rankings assist the editor but do not replace editorial judgment. Only approved articles are eligible for newsletter editions.

## Error Handling

The API client checks HTTP responses and converts backend/API failures into readable frontend errors.

The UI provides loading and retry states for API operations.

## Future Improvements

Potential production extensions include:

* Background job processing for ingestion and AI analysis
* Scheduled RSS ingestion
* Redis-backed task queues
* More advanced ranking signals
* Article content extraction when appropriate
* Newsletter email delivery
* Analytics
* Role-based permissions
* Database migrations with Alembic
* Observability and monitoring
* Rate limiting

These are intentionally outside the core MVP to keep the assessment implementation focused.

## Demo Flow

A simple end-to-end demonstration:

```text
1. Start Docker Compose
2. Open the Articles dashboard
3. Ingest an RSS feed
4. Show newly ingested PENDING articles
5. Run AI analysis on articles
6. Show categories, summaries, takeaways and relevance scores
7. Approve selected articles
8. Open Editions
9. Create a newsletter edition
10. Generate/select approved articles
11. Publish the edition
12. Open the public newsletter URL
```

## Engineering Highlights

This project demonstrates:

* Modular backend architecture
* REST API design
* Database modeling
* Idempotent ingestion
* AI integration with structured output
* Ranking logic
* Business-rule validation
* Human-in-the-loop workflow
* Automated tests
* Type-safe frontend API integration
* Dockerized development environment

## License

Add the license appropriate for this repository.
