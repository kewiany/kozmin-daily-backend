"""Remove club_id foreign key from news table

Revision ID: 021
Revises: 020
Create Date: 2026-04-12

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "021"
down_revision: Union[str, None] = "020"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("news_club_id_fkey", "news", type_="foreignkey")
    op.drop_column("news", "club_id")


def downgrade() -> None:
    op.add_column("news", sa.Column("club_id", sa.Integer(), nullable=True))
    op.create_foreign_key("news_club_id_fkey", "news", "clubs", ["club_id"], ["id"])
