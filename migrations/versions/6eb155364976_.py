"""empty message

Revision ID: 6eb155364976
Revises: 0f54183bb66f
Create Date: 2020-12-19 23:14:40.066581

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6eb155364976'
down_revision = '0f54183bb66f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='manager')
    op.drop_column('manager', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('manager', sa.Column('name', mysql.VARCHAR(length=255), nullable=False))
    op.create_index('name', 'manager', ['name'], unique=True)
    # ### end Alembic commands ###
