"""Add mode column, audience as ARRAY, short keys for audience/language

Revision ID: 013
Revises: 012
Create Date: 2026-04-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision: str = "013"
down_revision: Union[str, None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add mode column
    op.add_column("events", sa.Column("mode", sa.String(20), nullable=True))

    # 2. Convert audience from String to ARRAY(String)
    # First update existing values to short keys (still as plain string)
    op.execute("UPDATE events SET audience = 'open' WHERE LOWER(audience) = 'otwarte'")
    op.execute("UPDATE events SET audience = 'students' WHERE LOWER(audience) = 'studenci'")
    op.execute("UPDATE events SET audience = 'candidates' WHERE LOWER(audience) = 'kandydaci'")
    op.execute("UPDATE events SET audience = 'alumni' WHERE LOWER(audience) = 'absolwenci'")

    # Alter column type from VARCHAR to VARCHAR[] (ARRAY)
    op.execute(
        "ALTER TABLE events "
        "ALTER COLUMN audience TYPE VARCHAR(20)[] "
        "USING CASE WHEN audience IS NOT NULL THEN ARRAY[audience] ELSE NULL END"
    )

    # 3. Convert language to short keys
    op.execute("UPDATE events SET language = 'pl' WHERE LOWER(language) = 'polski'")
    op.execute("UPDATE events SET language = 'en' WHERE LOWER(language) = 'angielski'")


def downgrade() -> None:
    # Reverse language short keys
    op.execute("UPDATE events SET language = 'polski' WHERE language = 'pl'")
    op.execute("UPDATE events SET language = 'angielski' WHERE language = 'en'")

    # Convert audience ARRAY back to single string
    op.execute(
        "ALTER TABLE events "
        "ALTER COLUMN audience TYPE VARCHAR(50) "
        "USING audience[1]"
    )

    # Reverse audience short keys
    op.execute("UPDATE events SET audience = 'otwarte' WHERE audience = 'open'")
    op.execute("UPDATE events SET audience = 'studenci' WHERE audience = 'students'")
    op.execute("UPDATE events SET audience = 'kandydaci' WHERE audience = 'candidates'")
    op.execute("UPDATE events SET audience = 'absolwenci' WHERE audience = 'alumni'")

    # Drop mode column
    op.drop_column("events", "mode")
