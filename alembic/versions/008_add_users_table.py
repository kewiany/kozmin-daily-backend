"""Add users table for mobile app authentication

Revision ID: 008
Revises: 007
Create Date: 2026-03-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("apple_user_id", sa.String(255), nullable=False),
        sa.Column("email", sa.String(200), nullable=True),
        sa.Column("full_name", sa.String(200), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_users_apple_user_id", "users", ["apple_user_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_apple_user_id", table_name="users")
    op.drop_table("users")
