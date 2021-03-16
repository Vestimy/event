"""empty message

Revision ID: fedb9d5bd6c4
Revises: 1e4c1e6dceba
Create Date: 2021-03-16 19:51:57.976068

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fedb9d5bd6c4'
down_revision = '1e4c1e6dceba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('equipmentsubcategory', 'title',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('equipmentsubcategory', 'title',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
