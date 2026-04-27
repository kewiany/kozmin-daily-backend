"""Split discount description into short and long

Revision ID: 031
Revises: 030
Create Date: 2026-04-27

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "031"
down_revision: Union[str, None] = "030"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("discounts", "description", new_column_name="short_description")
    op.add_column("discounts", sa.Column("long_description", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("discounts", "long_description")
    op.alter_column("discounts", "short_description", new_column_name="description")
