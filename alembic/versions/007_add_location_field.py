"""Add address fields to events and initiatives

Revision ID: 007
Revises: 006
Create Date: 2026-03-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for table in ("events", "initiatives"):
        op.add_column(table, sa.Column("address_name", sa.String(300), nullable=True))
        op.add_column(table, sa.Column("address_street", sa.String(300), nullable=True))
        op.add_column(table, sa.Column("address_city", sa.String(200), nullable=True))
        op.add_column(table, sa.Column("room_number", sa.String(100), nullable=True))


def downgrade() -> None:
    for table in ("initiatives", "events"):
        op.drop_column(table, "room_number")
        op.drop_column(table, "address_city")
        op.drop_column(table, "address_street")
        op.drop_column(table, "address_name")
