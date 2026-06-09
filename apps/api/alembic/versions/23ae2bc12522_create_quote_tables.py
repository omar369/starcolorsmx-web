"""create quote tables

Revision ID: 23ae2bc12522
Revises:
Create Date: 2026-06-03 22:00:11.779210

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "23ae2bc12522"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "quote_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contact_value", sa.String(length=120), nullable=False),
        sa.Column("ip_hash", sa.String(length=128), nullable=True),
        sa.Column("user_agent_hash", sa.String(length=128), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quote_results_id"), "quote_results", ["id"])

    op.create_table(
        "quotes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_name", sa.String(length=100), nullable=False),
        sa.Column("contact_method", sa.String(length=20), nullable=False),
        sa.Column("contact_value", sa.String(length=120), nullable=False),
        sa.Column("state", sa.String(length=50), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("postal_code", sa.String(length=10), nullable=False),
        sa.Column("square_meters", sa.Float(), nullable=False),
        sa.Column("paint_product", sa.String(length=80), nullable=False),
        sa.Column("estimated_price", sa.Float(), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("result_json", sa.JSON(), nullable=False),
        sa.Column("user_type", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quotes_id"), "quotes", ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_quotes_id"), table_name="quotes")
    op.drop_table("quotes")
    op.drop_index(op.f("ix_quote_results_id"), table_name="quote_results")
    op.drop_table("quote_results")
