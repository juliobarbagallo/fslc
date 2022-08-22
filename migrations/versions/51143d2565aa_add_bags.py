"""Add bags

Revision ID: 51143d2565aa
Revises: 
Create Date: 2021-10-02 15:06:26.648786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "51143d2565aa"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bag_table = op.create_table(
        "bags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.bulk_insert(bag_table, [{"id": 1, "volume": 10}, {"id": 2, "volume": 20}])


def downgrade():
    op.drop_table("bags")
