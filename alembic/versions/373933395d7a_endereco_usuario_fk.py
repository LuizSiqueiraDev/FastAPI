"""endereco_usuario_fk

Revision ID: 373933395d7a
Revises: 
Create Date: 2022-09-22 12:59:44.243471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '373933395d7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('usuarios', sa.Column('endereco_id', sa.Integer(), nullable=True))
    op.create_foreign_key('endereco_usuario_fk', source_table='usuarios', referent_table='enderecos', local_cols=['endereco_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('endereco_usuario_fk', table_name='usuarios')
    op.drop_column('usuarios', 'endereco_id')