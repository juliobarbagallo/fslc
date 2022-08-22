"""Add cuboids

Revision ID: 833724243ce0
Revises: 51143d2565aa
Create Date: 2021-10-02 15:29:25.257388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "833724243ce0"
down_revision = "51143d2565aa"
branch_labels = None
depends_on = None


def upgrade():
    cuboids_table = op.create_table(
        "cuboids",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("depth", sa.Integer(), nullable=True),
        sa.Column("bag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bag_id"],
            ["bags.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.bulk_insert(
        cuboids_table,
        [
            {"id": 1, "width": 2, "height": 2, "depth": 2, "bag_id": 1},
            {"id": 2, "width": 3, "height": 2, "depth": 1, "bag_id": 2},
            {"id": 3, "width": 3, "height": 4, "depth": 2, "bag_id": 2},
        ],
    )


def downgrade():
    op.drop_table("cuboids")
