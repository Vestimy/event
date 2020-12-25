"""empty message

Revision ID: 1cc66685dede
Revises: a3e6d4092872
Create Date: 2020-12-26 01:34:50.533694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cc66685dede'
down_revision = 'a3e6d4092872'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('resource', sa.Binary(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 'resource')
    # ### end Alembic commands ###
