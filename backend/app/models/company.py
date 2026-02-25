from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    city: Mapped[str] = mapped_column(String(120), default="Caldas Novas")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="company")
    bookings = relationship("Booking", back_populates="company")
