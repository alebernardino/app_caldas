from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.repo = CompanyRepository(db)

    async def create(self, payload: CompanyCreate, user: User) -> Company:
        if user.role not in (UserRole.COMPANY, UserRole.ADMIN):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only company/admin")

        existing = await self.repo.get_by_owner(user.id)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company already exists")

        return await self.repo.create(
            Company(
                owner_user_id=user.id,
                name=payload.name,
                description=payload.description,
                city=payload.city,
            )
        )

    async def list_all(self) -> list[Company]:
        return await self.repo.list_all()

    async def update(self, company_id: UUID, payload: CompanyUpdate, user: User) -> Company:
        company = await self.repo.get(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        if user.role != UserRole.ADMIN and company.owner_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(company, key, value)

        await self.repo.db.commit()
        await self.repo.db.refresh(company)
        return company

    async def delete(self, company_id: UUID, user: User) -> None:
        company = await self.repo.get(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        if user.role != UserRole.ADMIN and company.owner_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        await self.repo.delete(company)
