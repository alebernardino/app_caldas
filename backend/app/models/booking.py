from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import BookingStatus


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id"), nullable=False, index=True)
    function_name: Mapped[str] = mapped_column(String(80), index=True)
    start_date: Mapped[date] = mapped_column(Date, index=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), default=BookingStatus.PENDING, index=True
    )
    season: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="bookings")
    provider = relationship("Provider", back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False)
