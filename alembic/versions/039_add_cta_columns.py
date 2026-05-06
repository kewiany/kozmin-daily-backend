"""Add CTA columns to events and news

Revision ID: 039
Revises: 038
Create Date: 2026-05-06

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "039"
down_revision: Union[str, None] = "038"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("events", sa.Column("cta_enabled", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("events", sa.Column("cta_button_text", sa.String(200), nullable=True))
    op.add_column("events", sa.Column("cta_link_url", sa.String(500), nullable=True))

    op.add_column("news", sa.Column("cta_enabled", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("news", sa.Column("cta_button_text", sa.String(200), nullable=True))
    op.add_column("news", sa.Column("cta_link_url", sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column("events", "cta_link_url")
    op.drop_column("events", "cta_button_text")
    op.drop_column("events", "cta_enabled")

    op.drop_column("news", "cta_link_url")
    op.drop_column("news", "cta_button_text")
    op.drop_column("news", "cta_enabled")
