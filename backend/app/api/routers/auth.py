from typing import Annotated

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenRefreshRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)
settings = get_settings()


@router.post("/register", response_model=TokenResponse)
@limiter.limit(settings.rate_limit_auth)
async def register(
    request: Request,
    payload: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    del request
    return await AuthService(db).register(payload)


@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.rate_limit_auth)
async def login(
    request: Request,
    payload: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    del request
    return await AuthService(db).login(payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    payload: TokenRefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    return await AuthService(db).refresh(payload.refresh_token)


@router.post("/logout")
async def logout(
    payload: TokenRefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    await AuthService(db).logout(payload.refresh_token)
    return {"message": "Logged out"}
