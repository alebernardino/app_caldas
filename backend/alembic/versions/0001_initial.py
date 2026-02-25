"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2026-02-25
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


user_role_enum = sa.Enum("ADMIN", "COMPANY", "PROVIDER", name="userrole")
booking_status_enum = sa.Enum(
    "PENDING", "ACCEPTED", "REJECTED", "CANCELED", "COMPLETED", name="bookingstatus"
)


def upgrade() -> None:
    user_role_enum.create(op.get_bind(), checkfirst=True)
    booking_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role_enum, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "companies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("owner_user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("owner_user_id"),
    )
    op.create_index(op.f("ix_companies_name"), "companies", ["name"], unique=False)

    op.create_table(
        "providers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("primary_function", sa.String(length=80), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("rating_average", sa.Float(), nullable=False),
        sa.Column("total_reviews", sa.Integer(), nullable=False),
        sa.Column("five_star_ratio", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(op.f("ix_providers_full_name"), "providers", ["full_name"], unique=False)
    op.create_index(op.f("ix_providers_is_available"), "providers", ["is_available"], unique=False)
    op.create_index(op.f("ix_providers_primary_function"), "providers", ["primary_function"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("jti", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_refresh_tokens_jti"), "refresh_tokens", ["jti"], unique=True)
    op.create_index(op.f("ix_refresh_tokens_user_id"), "refresh_tokens", ["user_id"], unique=False)

    op.create_table(
        "bookings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column("provider_id", sa.Uuid(), nullable=False),
        sa.Column("function_name", sa.String(length=80), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("status", booking_status_enum, nullable=False),
        sa.Column("season", sa.Boolean(), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bookings_company_id"), "bookings", ["company_id"], unique=False)
    op.create_index(op.f("ix_bookings_function_name"), "bookings", ["function_name"], unique=False)
    op.create_index(op.f("ix_bookings_provider_id"), "bookings", ["provider_id"], unique=False)
    op.create_index(op.f("ix_bookings_season"), "bookings", ["season"], unique=False)
    op.create_index(op.f("ix_bookings_start_date"), "bookings", ["start_date"], unique=False)
    op.create_index(op.f("ix_bookings_status"), "bookings", ["status"], unique=False)

    op.create_table(
        "reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("booking_id", sa.Uuid(), nullable=False),
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column("provider_id", sa.Uuid(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("rating >= 1 AND rating <= 5", name="review_rating_between_1_5"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("booking_id"),
    )
    op.create_index(op.f("ix_reviews_provider_id"), "reviews", ["provider_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_reviews_provider_id"), table_name="reviews")
    op.drop_table("reviews")

    op.drop_index(op.f("ix_bookings_status"), table_name="bookings")
    op.drop_index(op.f("ix_bookings_start_date"), table_name="bookings")
    op.drop_index(op.f("ix_bookings_season"), table_name="bookings")
    op.drop_index(op.f("ix_bookings_provider_id"), table_name="bookings")
    op.drop_index(op.f("ix_bookings_function_name"), table_name="bookings")
    op.drop_index(op.f("ix_bookings_company_id"), table_name="bookings")
    op.drop_table("bookings")

    op.drop_index(op.f("ix_refresh_tokens_user_id"), table_name="refresh_tokens")
    op.drop_index(op.f("ix_refresh_tokens_jti"), table_name="refresh_tokens")
    op.drop_table("refresh_tokens")

    op.drop_index(op.f("ix_providers_primary_function"), table_name="providers")
    op.drop_index(op.f("ix_providers_is_available"), table_name="providers")
    op.drop_index(op.f("ix_providers_full_name"), table_name="providers")
    op.drop_table("providers")

    op.drop_index(op.f("ix_companies_name"), table_name="companies")
    op.drop_table("companies")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    booking_status_enum.drop(op.get_bind(), checkfirst=True)
    user_role_enum.drop(op.get_bind(), checkfirst=True)
