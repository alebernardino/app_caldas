from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])


def serialize(booking) -> BookingResponse:
    return BookingResponse(
        id=booking.id,
        company_id=booking.company_id,
        provider_id=booking.provider_id,
        function_name=booking.function_name,
        start_date=booking.start_date,
        end_date=booking.end_date,
        status=booking.status,
        season=booking.season,
        requested_at=booking.requested_at,
    )


@router.post("", response_model=BookingResponse)
async def create_booking(
    payload: BookingCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> BookingResponse:
    item = await BookingService(db).create(payload, user)
    return serialize(item)


@router.post("/{booking_id}/accept", response_model=BookingResponse)
async def accept_booking(
    booking_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> BookingResponse:
    item = await BookingService(db).accept(booking_id, user)
    return serialize(item)


@router.post("/{booking_id}/reject", response_model=BookingResponse)
async def reject_booking(
    booking_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> BookingResponse:
    item = await BookingService(db).reject(booking_id, user)
    return serialize(item)


@router.post("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> BookingResponse:
    item = await BookingService(db).cancel(booking_id, user)
    return serialize(item)


@router.post("/{booking_id}/complete", response_model=BookingResponse)
async def complete_booking(
    booking_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> BookingResponse:
    item = await BookingService(db).complete(booking_id, user)
    return serialize(item)


@router.get("/company/{company_id}", response_model=list[BookingResponse])
async def list_company_bookings(
    company_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    season: bool = Query(default=False),
) -> list[BookingResponse]:
    items = await BookingService(db).list_company(company_id, user, season)
    return [serialize(item) for item in items]


@router.get("/provider/{provider_id}", response_model=list[BookingResponse])
async def list_provider_bookings(
    provider_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[BookingResponse]:
    items = await BookingService(db).list_provider(provider_id, user)
    return [serialize(item) for item in items]
