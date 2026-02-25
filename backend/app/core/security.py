from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenType:
    ACCESS = "access"
    REFRESH = "refresh"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _create_token(
    user_id: UUID,
    token_type: str,
    expires_delta: timedelta,
    jti: UUID | None = None,
) -> tuple[str, UUID, datetime]:
    settings = get_settings()
    token_jti = jti or uuid4()
    expire = datetime.now(UTC) + expires_delta
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "jti": str(token_jti),
        "exp": expire,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, token_jti, expire


def create_access_token(user_id: UUID) -> str:
    settings = get_settings()
    token, _, _ = _create_token(
        user_id=user_id,
        token_type=TokenType.ACCESS,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return token


def create_refresh_token(user_id: UUID) -> tuple[str, UUID, datetime]:
    settings = get_settings()
    return _create_token(
        user_id=user_id,
        token_type=TokenType.REFRESH,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
