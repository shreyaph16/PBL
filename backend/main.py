from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file into os.environ
load_dotenv()

from backend.core.config import settings
from backend.models.database import Base, engine
from backend.routers import analyze, reviews, products

# ── Create tables on startup (use Alembic for production migrations) ──────────
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sentiment Analysis API",
    description="ML-powered review sentiment pipeline",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(analyze.router)
app.include_router(reviews.router)
app.include_router(products.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Sentiment Analysis API is running. Check /docs for documentation.", "status": "ok"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}