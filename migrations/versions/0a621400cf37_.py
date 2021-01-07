"""empty message

Revision ID: 0a621400cf37
Revises: 570b178be2ec
Create Date: 2021-01-08 00:06:19.952985

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0a621400cf37'
down_revision = '570b178be2ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photoartist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photoartist',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('edit_imgarena', mysql.DATETIME(), nullable=True),
    sa.Column('created_imgarena', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
