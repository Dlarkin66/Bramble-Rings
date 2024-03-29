"""empty message

Revision ID: 878604df6ba7
Revises: 18f7e7923c90
Create Date: 2023-05-27 21:20:41.058986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '878604df6ba7'
down_revision = '18f7e7923c90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('order')

    # ### end Alembic commands ###
