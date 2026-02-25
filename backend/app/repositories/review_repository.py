from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, review: Review) -> Review:
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_by_booking(self, booking_id: UUID) -> Review | None:
        result = await self.db.execute(select(Review).where(Review.booking_id == booking_id))
        return result.scalar_one_or_none()

    async def list_by_provider(self, provider_id: UUID) -> list[Review]:
        result = await self.db.execute(select(Review).where(Review.provider_id == provider_id))
        return list(result.scalars().all())
