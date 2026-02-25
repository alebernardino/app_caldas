from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import BookingStatus


class BookingCreate(BaseModel):
    company_id: UUID
    provider_id: UUID
    function_name: str = Field(min_length=2, max_length=80)
    start_date: date
    end_date: date | None = None
    season: bool = False


class BookingStatusUpdate(BaseModel):
    status: BookingStatus


class BookingResponse(BaseModel):
    id: UUID
    company_id: UUID
    provider_id: UUID
    function_name: str
    start_date: date
    end_date: date | None
    status: BookingStatus
    season: bool
    requested_at: datetime
