"""Add is_pinned and priority to clubs and discounts

Revision ID: 030
Revises: 029
Create Date: 2026-04-27

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "030"
down_revision: Union[str, None] = "029"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clubs", sa.Column("is_pinned", sa.Boolean(), server_default="false", nullable=False))
    op.add_column("clubs", sa.Column("priority", sa.Integer(), server_default="0", nullable=False))
    op.add_column("discounts", sa.Column("is_pinned", sa.Boolean(), server_default="false", nullable=False))
    op.add_column("discounts", sa.Column("priority", sa.Integer(), server_default="0", nullable=False))


def downgrade() -> None:
    op.drop_column("discounts", "priority")
    op.drop_column("discounts", "is_pinned")
    op.drop_column("clubs", "priority")
    op.drop_column("clubs", "is_pinned")
