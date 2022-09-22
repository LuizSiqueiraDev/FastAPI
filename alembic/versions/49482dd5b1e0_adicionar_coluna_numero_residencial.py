"""adicionar coluna numero_residencial

Revision ID: 49482dd5b1e0
Revises: 5e2e05cac64d
Create Date: 2022-09-22 15:24:49.628735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49482dd5b1e0'
down_revision = '5e2e05cac64d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('enderecos', sa.Column('num_residencial', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('enderecos', 'num_residencial')
