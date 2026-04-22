from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func
from backend.models.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id         = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False, index=True)
    review_text  = Column(Text, nullable=False)
    sentiment    = Column(String(50), nullable=False)   # positive | negative | neutral
    confidence   = Column(Float, nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())