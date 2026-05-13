"""Seed university club for scraped events

Revision ID: 041
Revises: 040
Create Date: 2026-05-13

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "041"
down_revision: Union[str, None] = "040"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            INSERT INTO clubs (name, login, password, role, type, description, is_pinned, priority, is_archived, created_at)
            VALUES (
                'Akademia Leona Koźmińskiego',
                '__university__',
                '__no_login__',
                'club',
                'uczelnia',
                'Wydarzenia organizowane przez Akademię Leona Koźmińskiego',
                false,
                0,
                false,
                NOW()
            )
            ON CONFLICT (login) DO NOTHING
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM clubs WHERE login = '__university__'")
    )
