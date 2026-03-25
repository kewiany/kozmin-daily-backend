"""Add description, email, social URLs to clubs

Revision ID: 005
Revises: 004
Create Date: 2026-03-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clubs", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("clubs", sa.Column("email", sa.String(200), nullable=True))
    op.add_column("clubs", sa.Column("facebook_url", sa.String(500), nullable=True))
    op.add_column("clubs", sa.Column("instagram_url", sa.String(500), nullable=True))
    op.add_column("clubs", sa.Column("website_url", sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column("clubs", "website_url")
    op.drop_column("clubs", "instagram_url")
    op.drop_column("clubs", "facebook_url")
    op.drop_column("clubs", "email")
    op.drop_column("clubs", "description")
