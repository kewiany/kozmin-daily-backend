"""Add is_archived to events

Revision ID: 023
Revises: 022
"""

from alembic import op
import sqlalchemy as sa

revision = "023"
down_revision = "022"


def upgrade() -> None:
    op.add_column("events", sa.Column("is_archived", sa.Boolean(), server_default="false", nullable=False))


def downgrade() -> None:
    op.drop_column("events", "is_archived")
