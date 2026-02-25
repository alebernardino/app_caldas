from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    TokenType,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)
        self.tokens = TokenRepository(db)

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        existing = await self.users.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")

        user = User(
            email=payload.email,
            password_hash=get_password_hash(payload.password),
            role=payload.role,
        )
        created = await self.users.create(user)
        access = create_access_token(created.id)
        refresh, jti, expires_at = create_refresh_token(created.id)
        await self.tokens.create(
            RefreshToken(jti=jti, user_id=created.id, expires_at=expires_at, revoked=False)
        )
        return TokenResponse(access_token=access, refresh_token=refresh)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.users.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access = create_access_token(user.id)
        refresh, jti, expires_at = create_refresh_token(user.id)
        await self.tokens.create(RefreshToken(jti=jti, user_id=user.id, expires_at=expires_at, revoked=False))
        return TokenResponse(access_token=access, refresh_token=refresh)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            ) from exc
        if payload.get("type") != TokenType.REFRESH:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        token_jti = UUID(payload["jti"])
        user_id = UUID(payload["sub"])
        token_in_db = await self.tokens.get_by_jti(token_jti)
        if not token_in_db or token_in_db.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

        if token_in_db.expires_at < datetime.now(UTC):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        await self.tokens.revoke(token_in_db)
        access = create_access_token(user_id)
        new_refresh, new_jti, expires_at = create_refresh_token(user_id)
        await self.tokens.create(RefreshToken(jti=new_jti, user_id=user_id, expires_at=expires_at))
        return TokenResponse(access_token=access, refresh_token=new_refresh)

    async def logout(self, refresh_token: str) -> None:
        try:
            payload = decode_token(refresh_token)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            ) from exc
        if payload.get("type") != TokenType.REFRESH:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        token_jti = UUID(payload["jti"])
        token = await self.tokens.get_by_jti(token_jti)
        if token and not token.revoked:
            await self.tokens.revoke(token)
