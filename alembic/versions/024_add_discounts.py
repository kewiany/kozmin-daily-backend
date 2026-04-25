"""Add discounts table

Revision ID: 024
Revises: 023
"""

from alembic import op
import sqlalchemy as sa

revision = "024"
down_revision = "023"


def upgrade() -> None:
    op.create_table(
        "discounts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column("is_archived", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("discounts")
