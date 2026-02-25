from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.provider import Provider
from app.models.user import User
from app.repositories.provider_repository import ProviderRepository
from app.schemas.provider import ProviderCreate, ProviderUpdate


class ProviderService:
    def __init__(self, db: AsyncSession):
        self.repo = ProviderRepository(db)

    @staticmethod
    def concept(provider: Provider) -> str:
        return "5 estrelas" if provider.total_reviews > 0 and provider.five_star_ratio >= 0.7 else "em avaliação"

    async def create(self, payload: ProviderCreate, user: User) -> Provider:
        if user.role not in (UserRole.PROVIDER, UserRole.ADMIN):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only provider/admin")

        existing = await self.repo.get_by_user(user.id)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provider profile exists")

        return await self.repo.create(
            Provider(
                user_id=user.id,
                full_name=payload.full_name,
                primary_function=payload.primary_function,
                bio=payload.bio,
                is_available=payload.is_available,
            )
        )

    async def list_all(self) -> list[Provider]:
        return await self.repo.list_all()

    async def get(self, provider_id: UUID) -> Provider:
        provider = await self.repo.get(provider_id)
        if not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
        return provider

    async def update(self, provider_id: UUID, payload: ProviderUpdate, user: User) -> Provider:
        provider = await self.get(provider_id)
        if user.role != UserRole.ADMIN and provider.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(provider, key, value)

        await self.repo.db.commit()
        await self.repo.db.refresh(provider)
        return provider

    async def delete(self, provider_id: UUID, user: User) -> None:
        provider = await self.get(provider_id)
        if user.role != UserRole.ADMIN and provider.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        await self.repo.delete(provider)

    async def search(
        self,
        function_name: str | None,
        min_rating: float | None,
        only_five_star_concept: bool,
        is_available: bool | None,
    ) -> list[Provider]:
        providers = await self.repo.search(function_name, min_rating, is_available)
        if only_five_star_concept:
            providers = [p for p in providers if p.total_reviews > 0 and p.five_star_ratio >= 0.7]
        return providers
