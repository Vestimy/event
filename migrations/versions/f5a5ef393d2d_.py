"""empty message

Revision ID: f5a5ef393d2d
Revises: d93304ae4026
Create Date: 2021-01-07 23:49:33.924494

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f5a5ef393d2d'
down_revision = 'd93304ae4026'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('manager')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manager',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('edit_manager', mysql.DATETIME(), nullable=True),
    sa.Column('created_manager', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###