"""empty message

Revision ID: ba9e1b428cf8
Revises: 7c22a27ec53a
Create Date: 2020-11-25 00:25:40.090271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba9e1b428cf8'
down_revision = '7c22a27ec53a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('edit_equipment', sa.DateTime(), nullable=True),
    sa.Column('created_equipment', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('equipmentcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('edit_equipmentcategory', sa.DateTime(), nullable=True),
    sa.Column('created_equipmentcategory', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipmentcategory')
    op.drop_table('equipment')
    # ### end Alembic commands ###
