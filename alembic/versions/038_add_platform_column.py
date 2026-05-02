"""Add platform column to users

Revision ID: 038
Revises: 037
Create Date: 2026-05-02

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "038"
down_revision: Union[str, None] = "037"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("platform", sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "platform")
