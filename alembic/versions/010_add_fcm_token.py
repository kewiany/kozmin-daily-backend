"""Add fcm_token to users

Revision ID: 010
Revises: 009
Create Date: 2026-03-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("fcm_token", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "fcm_token")
