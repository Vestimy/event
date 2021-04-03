"""empty message

Revision ID: 367277e923c5
Revises: 0b321b9d7f26
Create Date: 2021-04-04 00:41:37.072969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '367277e923c5'
down_revision = '0b321b9d7f26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('privatemessages', sa.Column('message', sa.TEXT(length=300), nullable=True))
    op.add_column('privatemessages', sa.Column('subject', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('privatemessages', 'subject')
    op.drop_column('privatemessages', 'message')
    # ### end Alembic commands ###
