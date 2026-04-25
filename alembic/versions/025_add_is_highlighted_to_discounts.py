"""Add is_highlighted to discounts

Revision ID: 025
Revises: 024
"""

from alembic import op
import sqlalchemy as sa

revision = "025"
down_revision = "024"


def upgrade() -> None:
    op.add_column("discounts", sa.Column("is_highlighted", sa.Boolean(), server_default="false", nullable=False))


def downgrade() -> None:
    op.drop_column("discounts", "is_highlighted")
