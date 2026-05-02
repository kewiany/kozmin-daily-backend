"""Add profile info feature flags

Revision ID: 036
Revises: 035
Create Date: 2026-05-02

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "036"
down_revision: Union[str, None] = "035"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            "INSERT INTO feature_flags (key, value) VALUES (:key, :value)"
        ),
        [
            {"key": "profile_info_enabled", "value": "false"},
            {"key": "profile_info_text", "value": ""},
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM feature_flags WHERE key IN ('profile_info_enabled', 'profile_info_text')"
        )
    )
