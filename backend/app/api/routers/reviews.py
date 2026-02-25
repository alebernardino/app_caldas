from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])


def serialize(item) -> ReviewResponse:
    return ReviewResponse(
        id=item.id,
        booking_id=item.booking_id,
        company_id=item.company_id,
        provider_id=item.provider_id,
        rating=item.rating,
        comment=item.comment,
        created_at=item.created_at,
    )


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> ReviewResponse:
    review = await ReviewService(db).create(payload, user)
    return serialize(review)
