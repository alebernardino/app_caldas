from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProviderCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    primary_function: str = Field(min_length=2, max_length=80)
    bio: str | None = Field(default=None, max_length=1000)
    is_available: bool = True


class ProviderUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    primary_function: str | None = Field(default=None, min_length=2, max_length=80)
    bio: str | None = Field(default=None, max_length=1000)
    is_available: bool | None = None


class ProviderResponse(BaseModel):
    id: UUID
    user_id: UUID
    full_name: str
    primary_function: str
    bio: str | None
    is_available: bool
    rating_average: float
    total_reviews: int
    five_star_ratio: float
    concept: str
    created_at: datetime
