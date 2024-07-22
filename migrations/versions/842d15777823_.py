"""empty message

Revision ID: 842d15777823
Revises: 787560648ba2
Create Date: 2024-07-22 12:24:12.412604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '842d15777823'
down_revision = '787560648ba2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prestation', schema=None) as batch_op:
        batch_op.drop_index('ix_prestation_code')
        batch_op.create_index(batch_op.f('ix_prestation_code'), ['code'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prestation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_prestation_code'))
        batch_op.create_index('ix_prestation_code', ['code'], unique=True)

    # ### end Alembic commands ###
