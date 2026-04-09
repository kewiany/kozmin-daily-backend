"""Add feature_flags table

Revision ID: 017
Revises: 016
Create Date: 2026-04-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "017"
down_revision: Union[str, None] = "016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        "feature_flags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(100), unique=True, nullable=False),
        sa.Column("value", sa.String(500), nullable=False),
    )
    op.bulk_insert(table, [
        {"key": "game_enabled", "value": "true"},
        {"key": "game_url", "value": "https://kozmingame.vercel.app"},
        {"key": "developed_by", "value": "Samorząd Przyszłości 2026-2028"},
    ])


def downgrade() -> None:
    op.drop_table("feature_flags")
