from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    booking_id: UUID
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=3, max_length=1000)


class ReviewResponse(BaseModel):
    id: UUID
    booking_id: UUID
    company_id: UUID
    provider_id: UUID
    rating: int
    comment: str
    created_at: datetime
