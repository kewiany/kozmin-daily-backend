"""Add logo_url and type to clubs

Revision ID: 003
Revises: 002
Create Date: 2026-03-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clubs", sa.Column("logo_url", sa.String(500), nullable=True))
    op.add_column(
        "clubs", sa.Column("type", sa.String(20), server_default="club", nullable=False)
    )


def downgrade() -> None:
    op.drop_column("clubs", "type")
    op.drop_column("clubs", "logo_url")
