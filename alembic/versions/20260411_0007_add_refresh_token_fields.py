"""add refresh token fields to users

Revision ID: 20260411_0007
Revises: 20260411_0006
Create Date: 2026-04-11
"""

from alembic import op
import sqlalchemy as sa

revision = "20260411_0007"
down_revision = "20260411_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS refresh_token VARCHAR(255)")
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS refresh_token_updated_at TIMESTAMPTZ")
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_refresh_token ON users (refresh_token)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_users_refresh_token")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS refresh_token_updated_at")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS refresh_token")
