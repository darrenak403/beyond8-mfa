"""add user block fields

Revision ID: 20260411_0006
Revises: 20260411_0005
Create Date: 2026-04-11
"""

from alembic import op
import sqlalchemy as sa

revision = "20260411_0006"
down_revision = "20260411_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("blocked_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("blocked_reason", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("blocked_by_user_id", sa.String(length=36), nullable=True))

    op.create_index("ix_users_blocked_by_user_id", "users", ["blocked_by_user_id"], unique=False)
    op.create_foreign_key(
        "fk_users_blocked_by_user_id_users",
        "users",
        "users",
        ["blocked_by_user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_users_blocked_by_user_id_users", "users", type_="foreignkey")
    op.drop_index("ix_users_blocked_by_user_id", table_name="users")

    op.drop_column("users", "blocked_by_user_id")
    op.drop_column("users", "blocked_reason")
    op.drop_column("users", "blocked_at")
