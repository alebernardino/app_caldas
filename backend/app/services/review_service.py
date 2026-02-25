from statistics import mean

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import BookingStatus, UserRole
from app.models.review import Review
from app.models.user import User
from app.repositories.booking_repository import BookingRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.provider_repository import ProviderRepository
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.bookings = BookingRepository(db)
        self.companies = CompanyRepository(db)
        self.providers = ProviderRepository(db)
        self.reviews = ReviewRepository(db)

    async def create(self, payload: ReviewCreate, user: User) -> Review:
        booking = await self.bookings.get(payload.booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if booking.status != BookingStatus.COMPLETED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking must be completed")

        existing = await self.reviews.get_by_booking(payload.booking_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Review already exists")

        company = await self.companies.get(booking.company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        if user.role != UserRole.ADMIN and company.owner_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        review = await self.reviews.create(
            Review(
                booking_id=booking.id,
                company_id=booking.company_id,
                provider_id=booking.provider_id,
                rating=payload.rating,
                comment=payload.comment,
            )
        )

        await self._refresh_provider_scores(booking.provider_id)
        return review

    async def _refresh_provider_scores(self, provider_id) -> None:
        provider = await self.providers.get(provider_id)
        if not provider:
            return
        reviews = await self.reviews.list_by_provider(provider_id)
        if not reviews:
            provider.rating_average = 0
            provider.total_reviews = 0
            provider.five_star_ratio = 0
        else:
            ratings = [r.rating for r in reviews]
            provider.rating_average = float(mean(ratings))
            provider.total_reviews = len(ratings)
            five_stars = len([rating for rating in ratings if rating == 5])
            provider.five_star_ratio = five_stars / len(ratings)

        await self.db.commit()
        await self.db.refresh(provider)
