"""Add English translation columns to events, clubs, discounts, academic_calendar

Revision ID: 037
Revises: 036
Create Date: 2026-05-02

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "037"
down_revision: Union[str, None] = "036"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # events
    op.add_column("events", sa.Column("title_en", sa.String(300), nullable=True))
    op.add_column("events", sa.Column("description_en", sa.Text(), nullable=True))

    # clubs
    op.add_column("clubs", sa.Column("description_en", sa.Text(), nullable=True))
    op.add_column("clubs", sa.Column("type_en", sa.String(60), nullable=True))
    op.add_column("clubs", sa.Column("category_en", sa.String(100), nullable=True))

    # discounts
    op.add_column("discounts", sa.Column("title_en", sa.String(300), nullable=True))
    op.add_column("discounts", sa.Column("short_description_en", sa.Text(), nullable=True))
    op.add_column("discounts", sa.Column("long_description_en", sa.Text(), nullable=True))

    # academic_calendar
    op.add_column("academic_calendar", sa.Column("title_en", sa.String(200), nullable=True))


def downgrade() -> None:
    op.drop_column("academic_calendar", "title_en")

    op.drop_column("discounts", "long_description_en")
    op.drop_column("discounts", "short_description_en")
    op.drop_column("discounts", "title_en")

    op.drop_column("clubs", "category_en")
    op.drop_column("clubs", "type_en")
    op.drop_column("clubs", "description_en")

    op.drop_column("events", "description_en")
    op.drop_column("events", "title_en")
