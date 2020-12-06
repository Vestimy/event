"""empty message

Revision ID: 0c3d2b2b6b7e
Revises: da1d0ead96a6
Create Date: 2020-11-23 18:58:49.809869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c3d2b2b6b7e'
down_revision = 'da1d0ead96a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('time_event', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'time_event')
    # ### end Alembic commands ###
