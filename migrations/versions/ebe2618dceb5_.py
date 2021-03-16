"""empty message

Revision ID: ebe2618dceb5
Revises: 27d03c380909
Create Date: 2021-03-16 19:17:15.157496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebe2618dceb5'
down_revision = '27d03c380909'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equipment', sa.Column('name', sa.String(length=128), nullable=False))
    op.add_column('equipment', sa.Column('subcategory_id', sa.Integer(), nullable=True))
    op.add_column('equipment', sa.Column('title', sa.String(length=128), nullable=False))
    op.create_foreign_key(None, 'equipment', 'equipmentsubcategory', ['subcategory_id'], ['id'])
    op.add_column('equipmentcategory', sa.Column('title', sa.String(length=128), nullable=False))
    op.add_column('equipmentsubcategory', sa.Column('title', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('equipmentsubcategory', 'title')
    op.drop_column('equipmentcategory', 'title')
    op.drop_constraint(None, 'equipment', type_='foreignkey')
    op.drop_column('equipment', 'title')
    op.drop_column('equipment', 'subcategory_id')
    op.drop_column('equipment', 'name')
    # ### end Alembic commands ###
