from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.provider import ProviderResponse
from app.services.provider_service import ProviderService

router = APIRouter(prefix="/search", tags=["search"])


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


@router.get("/providers", response_model=list[ProviderResponse])
async def search_providers(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    function_name: str | None = Query(default=None),
    min_rating: float | None = Query(default=None, ge=0, le=5),
    only_five_star_concept: bool = Query(default=False),
    is_available: bool | None = Query(default=None),
) -> list[ProviderResponse]:
    del user
    items = await ProviderService(db).search(
        function_name=function_name,
        min_rating=min_rating,
        only_five_star_concept=only_five_star_concept,
        is_available=is_available,
    )
    return [serialize(item) for item in items]
