"""empty message

Revision ID: 0ef7b94b2e27
Revises: 946c65661cfa
Create Date: 2021-04-04 14:30:11.426850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ef7b94b2e27'
down_revision = '946c65661cfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('privatemessages', sa.Column('recipient_id', sa.Integer(), nullable=True))
    op.add_column('privatemessages', sa.Column('sender_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'privatemessages', 'users', ['recipient_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'privatemessages', type_='foreignkey')
    op.drop_column('privatemessages', 'sender_id')
    op.drop_column('privatemessages', 'recipient_id')
    # ### end Alembic commands ###
