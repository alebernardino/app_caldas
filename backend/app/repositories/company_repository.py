from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company


class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, company: Company) -> Company:
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def list_all(self) -> list[Company]:
        result = await self.db.execute(select(Company))
        return list(result.scalars().all())

    async def get(self, company_id: UUID) -> Company | None:
        result = await self.db.execute(select(Company).where(Company.id == company_id))
        return result.scalar_one_or_none()

    async def get_by_owner(self, owner_user_id: UUID) -> Company | None:
        result = await self.db.execute(select(Company).where(Company.owner_user_id == owner_user_id))
        return result.scalar_one_or_none()

    async def delete(self, company: Company) -> None:
        await self.db.delete(company)
        await self.db.commit()
