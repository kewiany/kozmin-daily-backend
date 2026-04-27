"""Add debata wyborcza event

Revision ID: 028
Revises: 027
Create Date: 2026-04-27

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "028"
down_revision: Union[str, None] = "027"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("""
        INSERT INTO events (title, description, start_date, start_time, end_date, end_time, status, event_type, mode, language, audience, address_name, is_highlighted, club_id)
        VALUES (
            'Debata Wyborcza',
            'Debata kandydatów na przewodniczącego Samorządu Studenckiego Akademii Leona Koźmińskiego. Przyjdź, posłuchaj programów kandydatów i zadaj pytania!',
            '2026-04-30', '16:00:00', '2026-04-30', '18:00:00',
            'approved', 'merit', 'offline', 'pl', ARRAY['open'],
            'Aula Leona Koźmińskiego', true, 1
        )
    """))


def downgrade() -> None:
    op.execute("DELETE FROM events WHERE title = 'Debata Wyborcza' AND start_date = '2026-04-30'")
