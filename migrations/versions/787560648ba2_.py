"""empty message

Revision ID: 787560648ba2
Revises: c2f0591c69d8
Create Date: 2024-07-19 11:41:19.710740

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '787560648ba2'
down_revision = 'c2f0591c69d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fiche_suivi', schema=None) as batch_op:
        batch_op.drop_constraint('fiche_suivi_ibfk_3', type_='foreignkey')
        batch_op.drop_column('prestation_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fiche_suivi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prestation_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('fiche_suivi_ibfk_3', 'prestation', ['prestation_id'], ['id'])

    # ### end Alembic commands ###
