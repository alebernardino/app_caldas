from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.provider import Provider


class ProviderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, provider: Provider) -> Provider:
        self.db.add(provider)
        await self.db.commit()
        await self.db.refresh(provider)
        return provider

    async def list_all(self) -> list[Provider]:
        result = await self.db.execute(select(Provider))
        return list(result.scalars().all())

    async def get(self, provider_id: UUID) -> Provider | None:
        result = await self.db.execute(select(Provider).where(Provider.id == provider_id))
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID) -> Provider | None:
        result = await self.db.execute(select(Provider).where(Provider.user_id == user_id))
        return result.scalar_one_or_none()

    async def search(
        self,
        function_name: str | None,
        min_rating: float | None,
        is_available: bool | None,
    ) -> list[Provider]:
        stmt = select(Provider)
        if function_name:
            stmt = stmt.where(Provider.primary_function.ilike(f"%{function_name}%"))
        if min_rating is not None:
            stmt = stmt.where(Provider.rating_average >= min_rating)
        if is_available is not None:
            stmt = stmt.where(Provider.is_available == is_available)

        result = await self.db.execute(stmt.order_by(Provider.rating_average.desc()))
        return list(result.scalars().all())

    async def delete(self, provider: Provider) -> None:
        await self.db.delete(provider)
        await self.db.commit()
