"""Add English translation fields to news

Revision ID: 034
Revises: 033
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = "034"
down_revision = "033"


def upgrade() -> None:
    op.add_column("news", sa.Column("title_en", sa.String(300), nullable=True))
    op.add_column("news", sa.Column("description_en", sa.Text(), nullable=True))
    op.add_column("news", sa.Column("preview_en", sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column("news", "preview_en")
    op.drop_column("news", "description_en")
    op.drop_column("news", "title_en")
