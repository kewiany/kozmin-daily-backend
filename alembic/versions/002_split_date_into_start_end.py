"""Split date into start_date, start_time, end_date, end_time

Revision ID: 002
Revises: 001
Create Date: 2026-03-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Events
    op.add_column("events", sa.Column("start_date", sa.Date(), nullable=True))
    op.add_column("events", sa.Column("start_time", sa.Time(), nullable=True))
    op.add_column("events", sa.Column("end_date", sa.Date(), nullable=True))
    op.add_column("events", sa.Column("end_time", sa.Time(), nullable=True))

    # Migrate existing data
    op.execute("""
        UPDATE events SET
            start_date = date::date,
            start_time = date::time,
            end_date = date::date,
            end_time = date::time
    """)

    # Set NOT NULL
    op.alter_column("events", "start_date", nullable=False)
    op.alter_column("events", "start_time", nullable=False)
    op.alter_column("events", "end_date", nullable=False)
    op.alter_column("events", "end_time", nullable=False)

    op.drop_column("events", "date")

    # Initiatives
    op.add_column("initiatives", sa.Column("start_date", sa.Date(), nullable=True))
    op.add_column("initiatives", sa.Column("start_time", sa.Time(), nullable=True))
    op.add_column("initiatives", sa.Column("end_date", sa.Date(), nullable=True))
    op.add_column("initiatives", sa.Column("end_time", sa.Time(), nullable=True))

    op.execute("""
        UPDATE initiatives SET
            start_date = date::date,
            start_time = date::time,
            end_date = date::date,
            end_time = date::time
    """)

    op.alter_column("initiatives", "start_date", nullable=False)
    op.alter_column("initiatives", "start_time", nullable=False)
    op.alter_column("initiatives", "end_date", nullable=False)
    op.alter_column("initiatives", "end_time", nullable=False)

    op.drop_column("initiatives", "date")


def downgrade() -> None:
    # Events
    op.add_column("events", sa.Column("date", sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE events SET date = (start_date + start_time)::timestamptz")
    op.alter_column("events", "date", nullable=False)
    op.drop_column("events", "start_date")
    op.drop_column("events", "start_time")
    op.drop_column("events", "end_date")
    op.drop_column("events", "end_time")

    # Initiatives
    op.add_column("initiatives", sa.Column("date", sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE initiatives SET date = (start_date + start_time)::timestamptz")
    op.alter_column("initiatives", "date", nullable=False)
    op.drop_column("initiatives", "start_date")
    op.drop_column("initiatives", "start_time")
    op.drop_column("initiatives", "end_date")
    op.drop_column("initiatives", "end_time")
