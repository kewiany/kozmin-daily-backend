"""Add firebase_uid column and make apple_user_id nullable

Revision ID: 015
Revises: 014
Create Date: 2026-04-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "015"
down_revision: Union[str, None] = "014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("firebase_uid", sa.String(255), nullable=True))
    op.create_unique_constraint("uq_users_firebase_uid", "users", ["firebase_uid"])
    op.alter_column("users", "apple_user_id", existing_type=sa.String(255), nullable=True)


def downgrade() -> None:
    op.alter_column("users", "apple_user_id", existing_type=sa.String(255), nullable=False)
    op.drop_constraint("uq_users_firebase_uid", "users", type_="unique")
    op.drop_column("users", "firebase_uid")
