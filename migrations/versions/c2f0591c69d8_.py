"""empty message

Revision ID: c2f0591c69d8
Revises: 7cbf19f7634e
Create Date: 2024-07-19 10:58:35.086119

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c2f0591c69d8'
down_revision = '7cbf19f7634e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('personne', schema=None) as batch_op:
        batch_op.alter_column('adresse',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=100),
               existing_nullable=True)

    with op.batch_alter_table('prestation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fiche_suivi_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=700), nullable=True))
        batch_op.create_index(batch_op.f('ix_prestation_description'), ['description'], unique=False)
        batch_op.create_foreign_key(None, 'fiche_suivi', ['fiche_suivi_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prestation', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_prestation_description'))
        batch_op.drop_column('description')
        batch_op.drop_column('fiche_suivi_id')

    with op.batch_alter_table('personne', schema=None) as batch_op:
        batch_op.alter_column('adresse',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=45),
               existing_nullable=True)

    # ### end Alembic commands ###
