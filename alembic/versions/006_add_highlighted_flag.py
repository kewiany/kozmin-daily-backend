"""Add is_highlighted flag to events and initiatives

Revision ID: 006
Revises: 005
Create Date: 2026-03-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column("is_highlighted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "initiatives",
        sa.Column("is_highlighted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )


def downgrade() -> None:
    op.drop_column("initiatives", "is_highlighted")
    op.drop_column("events", "is_highlighted")
