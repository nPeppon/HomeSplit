"""Initial tables: people, expenses

Revision ID: 0001_initial
Revises: 
Create Date: 2025-08-21
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "people",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
    )

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("category", sa.Text, nullable=False),
        sa.Column("paid_by", sa.Text, nullable=False),
        sa.Column("reimbursed_by", sa.Text, nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("description", sa.Text, server_default="", nullable=True),
    )


def downgrade() -> None:
    op.drop_table("expenses")
    op.drop_table("people")