"""empty message

Revision ID: 5f73503192af
Revises: 7eb118233657
Create Date: 2021-03-16 09:40:46.455858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f73503192af'
down_revision = '7eb118233657'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'company_id')
    # ### end Alembic commands ###