import logging
from sqlalchemy.orm import Session
from backend.models.orm_models import Review
from backend.models.schemas import ReviewCreate, ReviewResponse, AnalyzeResponse
from backend.services.ml_service import run_sentiment_analysis
from backend.core.exceptions import MLServiceError

logger = logging.getLogger(__name__)


def analyze_text(text: str) -> AnalyzeResponse:
    """Thin pass-through — keeps routers free of service imports."""
    return run_sentiment_analysis(text)


def create_review(db: Session, payload: ReviewCreate) -> ReviewResponse:
    """
    1. Run sentiment analysis on review_text.
    2. Persist the review + ML result to the DB.
    3. Return the stored ReviewResponse.
    """
    try:
        sentiment_result: AnalyzeResponse = run_sentiment_analysis(payload.review_text)
    except MLServiceError as exc:
        logger.error("ML failed for review creation: %s", exc)
        raise   # Let the router decide how to surface this

    db_review = Review(
        product_name=payload.product_name,
        review_text=payload.review_text,
        sentiment=sentiment_result.label,
        confidence=sentiment_result.confidence,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)   # Populates auto-generated fields (id, created_at)

    logger.info(
        "Stored review id=%s  product='%s'  sentiment=%s  confidence=%.3f",
        db_review.id, db_review.product_name,
        db_review.sentiment, db_review.confidence,
    )
    return ReviewResponse.model_validate(db_review)


def get_all_reviews(db: Session, skip: int = 0, limit: int = 100) -> list[ReviewResponse]:
    """Fetch paginated reviews, newest first."""
    rows = (
        db.query(Review)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [ReviewResponse.model_validate(row) for row in rows]