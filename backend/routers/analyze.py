from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from backend.models.schemas import AnalyzeRequest, AnalyzeResponse, ReviewCreate
from backend.services.review_service import create_review
from backend.models.database import get_db
from backend.services.ml_service import run_sentiment_analysis
from backend.core.exceptions import MLServiceError

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post(
    "",
    response_model=AnalyzeResponse,
    summary="Analyze a piece of text for sentiment",
)
def analyze(payload: AnalyzeRequest, db: Session = Depends(get_db)) -> AnalyzeResponse:
    """
    Accepts raw text, returns sentiment, and persists it to the database for the dashboard.
    """
    try:
        # First get the full analysis (with reasoning)
        result = run_sentiment_analysis(payload.text)
        
        # Then persist it as a review
        # We manually add to DB here to avoid double-analysis if we used create_review
        from backend.models.orm_models import Review
        db_review = Review(
            product_name="Quick Analyze",
            review_text=payload.text,
            sentiment=result.label,
            confidence=result.confidence
        )
        db.add(db_review)
        db.commit()
        
        return result
    except MLServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )