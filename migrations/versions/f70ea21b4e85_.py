"""empty message

Revision ID: f70ea21b4e85
Revises: 1db925066b13
Create Date: 2021-02-27 00:41:36.084394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f70ea21b4e85'
down_revision = '1db925066b13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rentalcompany', sa.Column('address', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rentalcompany', 'address')
    # ### end Alembic commands ###
