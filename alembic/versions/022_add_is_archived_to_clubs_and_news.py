"""Add is_archived to clubs and news

Revision ID: 022
Revises: 021
"""

from alembic import op
import sqlalchemy as sa

revision = "022"
down_revision = "021"


def upgrade() -> None:
    op.add_column("clubs", sa.Column("is_archived", sa.Boolean(), server_default="false", nullable=False))
    op.add_column("news", sa.Column("is_archived", sa.Boolean(), server_default="false", nullable=False))


def downgrade() -> None:
    op.drop_column("news", "is_archived")
    op.drop_column("clubs", "is_archived")
