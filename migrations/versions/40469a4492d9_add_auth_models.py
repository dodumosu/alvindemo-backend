"""add auth models

Revision ID: 40469a4492d9
Revises: 
Create Date: 2022-02-05 13:22:36.639363

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "40469a4492d9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "roles",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uid", sa.String(), nullable=False),
        sa.Column(
            "created",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("uid"),
    )
    op.create_table(
        "users",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.Column("current_login_at", sa.DateTime(), nullable=True),
        sa.Column("last_login_ip", sa.String(), nullable=True),
        sa.Column("current_login_ip", sa.String(), nullable=True),
        sa.Column("login_count", sa.Integer(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(), nullable=True),
        sa.Column("fs_uniquifier", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uid", sa.String(), nullable=False),
        sa.Column(
            "created",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("fs_uniquifier"),
        sa.UniqueConstraint("uid"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "roles_users",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "user_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("roles_users")
    op.drop_table("users")
    op.drop_table("roles")
    # ### end Alembic commands ###