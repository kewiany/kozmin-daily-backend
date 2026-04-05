"""Rename category to event_type with short keys

Revision ID: 012
Revises: 011
Create Date: 2026-04-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "012"
down_revision: Union[str, None] = "011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Drop old event_type column (had values like "konferencja")
    op.drop_column("events", "event_type")

    # 2. Rename category -> event_type
    op.alter_column("events", "category", new_column_name="event_type")

    # 3. Update Polish names to short keys
    op.execute("UPDATE events SET event_type = 'merit' WHERE event_type = 'Wydarzenie merytoryczne'")
    op.execute("UPDATE events SET event_type = 'fair' WHERE event_type = 'Targi'")
    op.execute("UPDATE events SET event_type = 'recruitment' WHERE event_type = 'Rekrutacja'")
    op.execute("UPDATE events SET event_type = 'integration' WHERE event_type = 'Integracja'")
    op.execute("UPDATE events SET event_type = 'sport' WHERE event_type = 'Wydarzenie sportowe'")


def downgrade() -> None:
    # Reverse short keys to Polish names
    op.execute("UPDATE events SET event_type = 'Wydarzenie merytoryczne' WHERE event_type = 'merit'")
    op.execute("UPDATE events SET event_type = 'Targi' WHERE event_type = 'fair'")
    op.execute("UPDATE events SET event_type = 'Rekrutacja' WHERE event_type = 'recruitment'")
    op.execute("UPDATE events SET event_type = 'Integracja' WHERE event_type = 'integration'")
    op.execute("UPDATE events SET event_type = 'Wydarzenie sportowe' WHERE event_type = 'sport'")

    # Rename event_type -> category
    op.alter_column("events", "event_type", new_column_name="category")

    # Re-add old event_type column
    op.add_column("events", sa.Column("event_type", sa.String(50), nullable=True))
