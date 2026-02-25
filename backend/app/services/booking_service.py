from datetime import date, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.company import Company
from app.models.enums import BookingStatus, UserRole
from app.models.provider import Provider
from app.models.user import User
from app.repositories.booking_repository import BookingRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.provider_repository import ProviderRepository
from app.schemas.booking import BookingCreate


class BookingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.bookings = BookingRepository(db)
        self.companies = CompanyRepository(db)
        self.providers = ProviderRepository(db)

    async def create(self, payload: BookingCreate, user: User) -> Booking:
        company = await self.companies.get(payload.company_id)
        provider = await self.providers.get(payload.provider_id)
        if not company or not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company or provider not found")

        if user.role != UserRole.ADMIN and company.owner_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        return await self.bookings.create(
            Booking(
                company_id=payload.company_id,
                provider_id=payload.provider_id,
                function_name=payload.function_name,
                start_date=payload.start_date,
                end_date=payload.end_date,
                season=payload.season,
                status=BookingStatus.PENDING,
            )
        )

    @staticmethod
    def _week_bounds(target_date: date) -> tuple[date, date]:
        start = target_date - timedelta(days=target_date.weekday())
        end = start + timedelta(days=6)
        return start, end

    async def accept(self, booking_id: UUID, user: User) -> Booking:
        booking = await self.bookings.get(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

        provider = await self.providers.get(booking.provider_id)
        if not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

        if user.role != UserRole.ADMIN and provider.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        week_start, week_end = self._week_bounds(booking.start_date)
        count = await self.bookings.count_provider_accepted_in_range(
            booking.provider_id, week_start, week_end
        )
        if booking.status != BookingStatus.ACCEPTED and count >= 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provider reached weekly limit (2 bookings)",
            )

        booking.status = BookingStatus.ACCEPTED
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def reject(self, booking_id: UUID, user: User) -> Booking:
        booking = await self.bookings.get(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

        provider = await self.providers.get(booking.provider_id)
        if not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

        if user.role != UserRole.ADMIN and provider.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        booking.status = BookingStatus.REJECTED
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def cancel(self, booking_id: UUID, user: User) -> Booking:
        booking = await self.bookings.get(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

        company = await self.companies.get(booking.company_id)
        provider = await self.providers.get(booking.provider_id)
        if not company or not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Related entities not found")

        is_owner = company.owner_user_id == user.id or provider.user_id == user.id
        if user.role != UserRole.ADMIN and not is_owner:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        booking.status = BookingStatus.CANCELED
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def complete(self, booking_id: UUID, user: User) -> Booking:
        booking = await self.bookings.get(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

        company = await self.companies.get(booking.company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        if user.role != UserRole.ADMIN and company.owner_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        booking.status = BookingStatus.COMPLETED
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def list_company(self, company_id: UUID, user: User, season: bool) -> list[Booking]:
        company = await self.companies.get(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        if user.role != UserRole.ADMIN and company.owner_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        items = await self.bookings.list_for_company(company_id)
        if season:
            return sorted(items, key=lambda b: (b.start_date - b.requested_at.date()).days, reverse=True)
        return sorted(items, key=lambda b: b.requested_at)

    async def list_provider(self, provider_id: UUID, user: User) -> list[Booking]:
        provider = await self.providers.get(provider_id)
        if not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
        if user.role != UserRole.ADMIN and provider.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        items = await self.bookings.list_for_provider(provider_id)
        return sorted(items, key=lambda b: b.start_date)
