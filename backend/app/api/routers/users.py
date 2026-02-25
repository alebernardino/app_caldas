from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserMeResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
async def me(user: Annotated[User, Depends(get_current_user)]) -> UserMeResponse:
    return UserMeResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
    )
