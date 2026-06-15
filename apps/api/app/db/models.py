from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_method: Mapped[str] = mapped_column(String(20), nullable=False)
    contact_value: Mapped[str] = mapped_column(String(120), nullable=False)

    state: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(10), nullable=False)

    square_meters: Mapped[float] = mapped_column(Float, nullable=False)
    paint_product: Mapped[str] = mapped_column(String(80), nullable=False)
    estimated_price: Mapped[float] = mapped_column(Float, nullable=False)

    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    result_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    user_type: Mapped[str] = mapped_column(
        String(20),
        default="visitor",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="created",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class QuoteRequest(Base):
    __tablename__ = "quote_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    contact_value: Mapped[str] = mapped_column(String(120), nullable=False)
    ip_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    user_agent_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)

    reason: Mapped[str] = mapped_column(Text, default="quote_created")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
