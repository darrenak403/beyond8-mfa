"""add explanation column to questions

Revision ID: 20260813_0020
Revises: 20260501_0019
Create Date: 2026-08-13
"""

from alembic import op

revision = "20260813_0020"
down_revision = "20260501_0019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE questions ADD COLUMN IF NOT EXISTS explanation TEXT")


def downgrade() -> None:
    op.execute("ALTER TABLE questions DROP COLUMN IF EXISTS explanation")
