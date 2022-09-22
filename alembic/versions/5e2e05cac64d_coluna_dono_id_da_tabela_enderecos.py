"""coluna dono_id da tabela enderecos

Revision ID: 5e2e05cac64d
Revises: 373933395d7a
Create Date: 2022-09-22 14:55:20.479561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e2e05cac64d'
down_revision = '373933395d7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('enderecos', sa.Column('dono_id', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('enderecos', 'dono_id')
