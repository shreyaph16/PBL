from fastapi import HTTPException, status


class MLServiceError(Exception):
    """Raised when the ML pipeline returns an unexpected result."""
    pass


class ReviewNotFoundError(Exception):
    """Raised when a review cannot be located in the DB."""
    pass


# ── HTTP helpers (call these inside routers) ───────────────────────────────────

def raise_ml_error(detail: str = "Sentiment analysis failed."):
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


def raise_not_found(detail: str = "Review not found."):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def raise_bad_request(detail: str = "Invalid input."):
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)