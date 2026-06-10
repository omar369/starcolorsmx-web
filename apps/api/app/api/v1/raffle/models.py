from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class Raffle(Base):
    __tablename__ = "raffles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(120), unique=True, index=True, nullable=False
    )

    prize_title: Mapped[str | None] = mapped_column(String(160), nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)

    total_numbers: Mapped[int] = mapped_column(Integer, default=495, nullable=False)
    numbers_per_branch: Mapped[int] = mapped_column(
        Integer, default=165, nullable=False
    )

    max_codes_per_batch: Mapped[int] = mapped_column(
        Integer, default=10, nullable=False
    )
    max_batches_per_user_24h: Mapped[int] = mapped_column(
        Integer, default=10, nullable=False
    )

    starts_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
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


class RaffleBranch(Base):
    __tablename__ = "raffle_branches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    raffle_id: Mapped[int] = mapped_column(
        ForeignKey("raffles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    number_start: Mapped[int] = mapped_column(Integer, nullable=False)
    number_end: Mapped[int] = mapped_column(Integer, nullable=False)

    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("raffle_id", "slug", name="uq_raffle_branches_raffle_slug"),
    )


class RaffleNumber(Base):
    __tablename__ = "raffle_numbers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    raffle_id: Mapped[int] = mapped_column(
        ForeignKey("raffles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("raffle_branches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    number: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(String(20), default="available", nullable=False)

    taken_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    taken_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("raffle_id", "number", name="uq_raffle_numbers_raffle_number"),
        Index(
            "ix_raffle_numbers_raffle_branch_status", "raffle_id", "branch_id", "status"
        ),
    )


class RaffleTicketCode(Base):
    __tablename__ = "raffle_ticket_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    raffle_id: Mapped[int] = mapped_column(
        ForeignKey("raffles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    code_hash: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    code_last4: Mapped[str] = mapped_column(String(12), nullable=False)

    status: Mapped[str] = mapped_column(String(20), default="available", nullable=False)

    used_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    __table_args__ = (
        Index("ix_raffle_ticket_codes_raffle_status", "raffle_id", "status"),
    )


class RaffleTicketBatch(Base):
    __tablename__ = "raffle_ticket_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    raffle_id: Mapped[int] = mapped_column(
        ForeignKey("raffles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("raffle_branches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

    submitted_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    accepted_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rejected_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    status: Mapped[str] = mapped_column(String(20), default="validated", nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    items: Mapped[list["RaffleTicketBatchItem"]] = relationship(
        back_populates="batch",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_raffle_ticket_batches_user_created", "user_id", "created_at"),
        Index("ix_raffle_ticket_batches_ip_created", "ip_address", "created_at"),
    )


class RaffleTicketBatchItem(Base):
    __tablename__ = "raffle_ticket_batch_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    batch_id: Mapped[int] = mapped_column(
        ForeignKey("raffle_ticket_batches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ticket_code_id: Mapped[int | None] = mapped_column(
        ForeignKey("raffle_ticket_codes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    code_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    code_last4: Mapped[str] = mapped_column(String(12), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(80), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    batch: Mapped["RaffleTicketBatch"] = relationship(back_populates="items")


class RaffleEntry(Base):
    __tablename__ = "raffle_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    raffle_id: Mapped[int] = mapped_column(
        ForeignKey("raffles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("raffle_branches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ticket_code_id: Mapped[int] = mapped_column(
        ForeignKey("raffle_ticket_codes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    raffle_number_id: Mapped[int] = mapped_column(
        ForeignKey("raffle_numbers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("raffle_ticket_batches.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    selected_number: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "raffle_id", "ticket_code_id", name="uq_raffle_entries_ticket_code"
        ),
        UniqueConstraint(
            "raffle_id", "raffle_number_id", name="uq_raffle_entries_number_id"
        ),
        UniqueConstraint(
            "raffle_id", "selected_number", name="uq_raffle_entries_selected_number"
        ),
        Index("ix_raffle_entries_user_created", "user_id", "created_at"),
    )
