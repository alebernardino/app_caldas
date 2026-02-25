import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    COMPANY = "company"
    PROVIDER = "provider"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELED = "canceled"
    COMPLETED = "completed"
