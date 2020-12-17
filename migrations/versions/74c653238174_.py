"""empty message

Revision ID: 74c653238174
Revises: 9351400cff88
Create Date: 2020-12-17 20:19:08.824604

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '74c653238174'
down_revision = '9351400cff88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('arena', sa.Column('address', sa.String(length=255), nullable=True))
    op.drop_column('arena', 'adres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('arena', sa.Column('adres', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('arena', 'address')
    # ### end Alembic commands ###
