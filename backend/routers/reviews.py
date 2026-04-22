from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.schemas import ReviewCreate, ReviewResponse
from backend.services.review_service import create_review, get_all_reviews
from backend.core.exceptions import MLServiceError

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get(
    "",
    response_model=list[ReviewResponse],
    summary="Fetch all stored reviews",
)
def list_reviews(
    skip:  int = Query(default=0,   ge=0,  description="Offset"),
    limit: int = Query(default=100, ge=1, le=500, description="Page size"),
    db: Session = Depends(get_db),
) -> list[ReviewResponse]:
    return get_all_reviews(db, skip=skip, limit=limit)


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a review — runs sentiment analysis and persists result",
)
def submit_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
) -> ReviewResponse:
    try:
        return create_review(db, payload)
    except MLServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Sentiment analysis unavailable: {exc}",
        )