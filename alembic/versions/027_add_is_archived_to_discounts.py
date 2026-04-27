"""Add is_archived to discounts

Revision ID: 027
Revises: 026
"""

from alembic import op
import sqlalchemy as sa

revision = "027"
down_revision = "026"


def upgrade() -> None:
    op.add_column("discounts", sa.Column("is_archived", sa.Boolean(), server_default="false", nullable=False))


def downgrade() -> None:
    op.drop_column("discounts", "is_archived")
