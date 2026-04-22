from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ── /analyze ──────────────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to analyze")


class AnalyzeResponse(BaseModel):
    label:      str   = Field(..., description="positive | negative | neutral")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning:  Optional[str] = Field(None, description="AI-generated summary of the sentiment")


class ProductResponse(BaseModel):
    products: list[str]


# ── /reviews ───────────────────────────────────────────────────────────────────

class ReviewCreate(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=255)
    review_text:  str = Field(..., min_length=1, max_length=5000)


class ReviewResponse(BaseModel):
    id:           int
    product_name: str
    review_text:  str
    sentiment:    str
    confidence:   float
    created_at:   Optional[datetime] = None

    model_config = {"from_attributes": True}   # Pydantic v2 ORM mode