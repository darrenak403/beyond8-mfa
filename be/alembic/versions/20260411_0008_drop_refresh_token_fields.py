"""drop refresh token fields from users

Revision ID: 20260411_0008
Revises: 20260411_0007
Create Date: 2026-04-11
"""

from alembic import op

revision = "20260411_0008"
down_revision = "20260411_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_users_refresh_token")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS refresh_token_updated_at")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS refresh_token")


def downgrade() -> None:
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS refresh_token VARCHAR(255)")
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS refresh_token_updated_at TIMESTAMPTZ")
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_refresh_token ON users (refresh_token)")
