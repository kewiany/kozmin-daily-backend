"""Add is_pinned and priority to news

Revision ID: 035
Revises: 034
Create Date: 2026-05-02

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "035"
down_revision: Union[str, None] = "034"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("news", sa.Column("is_pinned", sa.Boolean(), server_default="false", nullable=False))
    op.add_column("news", sa.Column("priority", sa.Integer(), server_default="0", nullable=False))


def downgrade() -> None:
    op.drop_column("news", "priority")
    op.drop_column("news", "is_pinned")
