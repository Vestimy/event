"""empty message

Revision ID: b6e4a8bc6870
Revises: a2dae3ef7f72
Create Date: 2021-01-07 21:57:23.399495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6e4a8bc6870'
down_revision = 'a2dae3ef7f72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'description')
    # ### end Alembic commands ###
