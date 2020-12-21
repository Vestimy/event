"""empty message

Revision ID: f647914b0f67
Revises: 02890c76b174
Create Date: 2020-12-18 13:38:48.837027

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f647914b0f67'
down_revision = '02890c76b174'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('typeevent_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event', 'typeevent', ['typeevent_id'], ['id'])
    op.drop_constraint('typeevent_ibfk_1', 'typeevent', type_='foreignkey')
    op.drop_column('typeevent', 'event_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('typeevent', sa.Column('event_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('typeevent_ibfk_1', 'typeevent', 'event', ['event_id'], ['id'])
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'typeevent_id')
    # ### end Alembic commands ###