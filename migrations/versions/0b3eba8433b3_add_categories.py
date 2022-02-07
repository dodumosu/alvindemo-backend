"""Add categories

Revision ID: 0b3eba8433b3
Revises: 95261faba23a
Create Date: 2022-02-06 23:31:42.082799

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0b3eba8433b3"
down_revision = "95261faba23a"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO categories(name) VALUES ('Groceries')")
    op.execute("INSERT INTO categories(name) VALUES ('Transport')")
    op.execute("INSERT INTO categories(name) VALUES ('Miscellaneous')")
    op.execute("INSERT INTO categories(name) VALUES ('Savings')")


def downgrade():
    op.execute("DELETE FROM categories WHERE name = 'Groceries'")
    op.execute("DELETE FROM categories WHERE name = 'Transport'")
    op.execute("DELETE FROM categories WHERE name = 'Miscellaneous'")
    op.execute("DELETE FROM categories WHERE name = 'Savings'")
