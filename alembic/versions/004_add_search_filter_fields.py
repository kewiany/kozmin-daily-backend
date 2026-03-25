"""Add audience, event_type, language to events and initiatives

Revision ID: 004
Revises: 003
Create Date: 2026-03-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("events", sa.Column("audience", sa.String(50), nullable=True))
    op.add_column("events", sa.Column("event_type", sa.String(50), nullable=True))
    op.add_column("events", sa.Column("language", sa.String(50), nullable=True))

    op.add_column("initiatives", sa.Column("audience", sa.String(50), nullable=True))
    op.add_column("initiatives", sa.Column("event_type", sa.String(50), nullable=True))
    op.add_column("initiatives", sa.Column("language", sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column("initiatives", "language")
    op.drop_column("initiatives", "event_type")
    op.drop_column("initiatives", "audience")

    op.drop_column("events", "language")
    op.drop_column("events", "event_type")
    op.drop_column("events", "audience")
