from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.provider import ProviderCreate, ProviderResponse, ProviderUpdate
from app.services.provider_service import ProviderService

router = APIRouter(prefix="/providers", tags=["providers"])


def serialize(provider) -> ProviderResponse:
    return ProviderResponse(
        id=provider.id,
        user_id=provider.user_id,
        full_name=provider.full_name,
        primary_function=provider.primary_function,
        bio=provider.bio,
        is_available=provider.is_available,
        rating_average=provider.rating_average,
        total_reviews=provider.total_reviews,
        five_star_ratio=provider.five_star_ratio,
        concept=ProviderService.concept(provider),
        created_at=provider.created_at,
    )


@router.post("", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_provider(
    payload: ProviderCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> ProviderResponse:
    provider = await ProviderService(db).create(payload, user)
    return serialize(provider)


@router.get("", response_model=list[ProviderResponse])
async def list_providers(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[ProviderResponse]:
    del user
    providers = await ProviderService(db).list_all()
    return [serialize(item) for item in providers]


@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(
    provider_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> ProviderResponse:
    del user
    provider = await ProviderService(db).get(provider_id)
    return serialize(provider)


@router.put("/{provider_id}", response_model=ProviderResponse)
async def update_provider(
    provider_id: UUID,
    payload: ProviderUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> ProviderResponse:
    provider = await ProviderService(db).update(provider_id, payload, user)
    return serialize(provider)


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_provider(
    provider_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Response:
    await ProviderService(db).delete(provider_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
