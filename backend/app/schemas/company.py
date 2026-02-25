from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    city: str = Field(default="Caldas Novas", min_length=2, max_length=120)


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    city: str | None = Field(default=None, min_length=2, max_length=120)


class CompanyResponse(BaseModel):
    id: UUID
    owner_user_id: UUID
    name: str
    description: str | None
    city: str
    created_at: datetime
