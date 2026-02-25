from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), index=True)
    primary_function: Mapped[str] = mapped_column(String(80), index=True)
    bio: Mapped[str | None] = mapped_column(Text(), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    rating_average: Mapped[float] = mapped_column(Float, default=0)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)
    five_star_ratio: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="provider")
    bookings = relationship("Booking", back_populates="provider")
    reviews = relationship("Review", back_populates="provider")
