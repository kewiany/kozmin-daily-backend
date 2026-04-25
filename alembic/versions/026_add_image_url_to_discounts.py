"""Add image_url to discounts

Revision ID: 026
Revises: 025
"""

from alembic import op
import sqlalchemy as sa

revision = "026"
down_revision = "025"


def upgrade() -> None:
    op.add_column("discounts", sa.Column("image_url", sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column("discounts", "image_url")
