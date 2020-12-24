"""empty message

Revision ID: 34246ea2315f
Revises: 
Create Date: 2020-12-24 10:46:56.862329

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '34246ea2315f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('arena_city')
    op.alter_column('artist', 'first_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('artist', 'last_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'last_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('artist', 'first_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_table('arena_city',
    sa.Column('city_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('arena_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['arena_id'], ['arena.id'], name='arena_city_ibfk_2'),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], name='arena_city_ibfk_1'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###