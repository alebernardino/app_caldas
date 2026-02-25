from datetime import date
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.enums import BookingStatus


class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def get(self, booking_id: UUID) -> Booking | None:
        result = await self.db.execute(select(Booking).where(Booking.id == booking_id))
        return result.scalar_one_or_none()

    async def list_for_company(self, company_id: UUID) -> list[Booking]:
        result = await self.db.execute(select(Booking).where(Booking.company_id == company_id))
        return list(result.scalars().all())

    async def list_for_provider(self, provider_id: UUID) -> list[Booking]:
        result = await self.db.execute(select(Booking).where(Booking.provider_id == provider_id))
        return list(result.scalars().all())

    async def count_provider_accepted_in_range(
        self,
        provider_id: UUID,
        start: date,
        end: date,
    ) -> int:
        result = await self.db.execute(
            select(Booking).where(
                and_(
                    Booking.provider_id == provider_id,
                    Booking.status.in_([BookingStatus.ACCEPTED, BookingStatus.COMPLETED]),
                    Booking.start_date >= start,
                    Booking.start_date <= end,
                )
            )
        )
        return len(result.scalars().all())
