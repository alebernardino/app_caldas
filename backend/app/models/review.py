from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    booking_id: Mapped[UUID] = mapped_column(ForeignKey("bookings.id"), unique=True, nullable=False)
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (CheckConstraint("rating >= 1 AND rating <= 5", name="review_rating_between_1_5"),)

    booking = relationship("Booking", back_populates="review")
    provider = relationship("Provider", back_populates="reviews")
