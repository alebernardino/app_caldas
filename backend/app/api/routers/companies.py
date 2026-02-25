from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


def serialize(company) -> CompanyResponse:
    return CompanyResponse(
        id=company.id,
        owner_user_id=company.owner_user_id,
        name=company.name,
        description=company.description,
        city=company.city,
        created_at=company.created_at,
    )


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    payload: CompanyCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> CompanyResponse:
    company = await CompanyService(db).create(payload, user)
    return serialize(company)


@router.get("", response_model=list[CompanyResponse])
async def list_companies(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[CompanyResponse]:
    del user
    items = await CompanyService(db).list_all()
    return [serialize(item) for item in items]


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: UUID,
    payload: CompanyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> CompanyResponse:
    item = await CompanyService(db).update(company_id, payload, user)
    return serialize(item)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Response:
    await CompanyService(db).delete(company_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
