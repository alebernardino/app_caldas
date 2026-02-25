from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token

    async def get_by_jti(self, jti: UUID) -> RefreshToken | None:
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        return result.scalar_one_or_none()

    async def revoke(self, token: RefreshToken) -> None:
        token.revoked = True
        await self.db.commit()

    async def cleanup_expired(self, now: datetime) -> None:
        await self.db.execute(delete(RefreshToken).where(RefreshToken.expires_at < now))
        await self.db.commit()
