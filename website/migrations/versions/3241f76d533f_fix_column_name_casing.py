"""Fix column name casing

Revision ID: 3241f76d533f
Revises: fc9c9c1dbbe7
Create Date: 2024-11-22 13:38:30.490762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3241f76d533f'
down_revision = 'fc9c9c1dbbe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Name', sa.String(length=100), nullable=False))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.drop_column('Name')

    # ### end Alembic commands ###
