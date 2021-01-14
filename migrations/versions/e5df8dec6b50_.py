"""empty message

Revision ID: e5df8dec6b50
Revises: eb5ed182661f
Create Date: 2021-01-09 22:04:49.070797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5df8dec6b50'
down_revision = 'eb5ed182661f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('arena', sa.Column('url', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('arena', 'url')
    # ### end Alembic commands ###
