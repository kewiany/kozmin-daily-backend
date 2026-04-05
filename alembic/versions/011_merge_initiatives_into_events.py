"""Merge initiatives into events table

Revision ID: 011
Revises: 010
Create Date: 2026-04-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("events", sa.Column("category", sa.String(100), nullable=True))

    op.execute("""
        INSERT INTO events (
            title, description, category,
            start_date, start_time, end_date, end_time,
            status, audience, event_type, language,
            address_name, address_street, address_city, room_number,
            is_highlighted, club_id, created_at
        )
        SELECT
            title, description, category,
            start_date, start_time, end_date, end_time,
            status, audience, event_type, language,
            address_name, address_street, address_city, room_number,
            is_highlighted, club_id, created_at
        FROM initiatives
    """)

    op.drop_table("initiatives")


def downgrade() -> None:
    op.create_table(
        "initiatives",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("start_time", sa.Time, nullable=False),
        sa.Column("end_date", sa.Date, nullable=False),
        sa.Column("end_time", sa.Time, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("audience", sa.String(50), nullable=True),
        sa.Column("event_type", sa.String(50), nullable=True),
        sa.Column("language", sa.String(50), nullable=True),
        sa.Column("address_name", sa.String(300), nullable=True),
        sa.Column("address_street", sa.String(300), nullable=True),
        sa.Column("address_city", sa.String(200), nullable=True),
        sa.Column("room_number", sa.String(100), nullable=True),
        sa.Column("is_highlighted", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("club_id", sa.Integer, sa.ForeignKey("clubs.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.execute("""
        INSERT INTO initiatives (
            title, description, category,
            start_date, start_time, end_date, end_time,
            status, audience, event_type, language,
            address_name, address_street, address_city, room_number,
            is_highlighted, club_id, created_at
        )
        SELECT
            title, description, category,
            start_date, start_time, end_date, end_time,
            status, audience, event_type, language,
            address_name, address_street, address_city, room_number,
            is_highlighted, club_id, created_at
        FROM events
        WHERE category IS NOT NULL
    """)

    op.execute("DELETE FROM events WHERE category IS NOT NULL")
    op.drop_column("events", "category")
