"""Add preview to news

Revision ID: 033
Revises: 032
Create Date: 2026-04-28
"""

from alembic import op
import sqlalchemy as sa

revision = "033"
down_revision = "032"


def upgrade() -> None:
    op.add_column("news", sa.Column("preview", sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column("news", "preview")
