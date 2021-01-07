"""empty message

Revision ID: d93304ae4026
Revises: b6e4a8bc6870
Create Date: 2021-01-07 23:49:04.333481

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd93304ae4026'
down_revision = 'b6e4a8bc6870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('managerphoto_ibfk_1', 'managerphoto', type_='foreignkey')
    op.drop_column('managerphoto', 'manager_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('managerphoto', sa.Column('manager_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('managerphoto_ibfk_1', 'managerphoto', 'manager', ['manager_id'], ['id'])
    # ### end Alembic commands ###
