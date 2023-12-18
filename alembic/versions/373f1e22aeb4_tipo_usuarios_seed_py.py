"""tipo_usuarios_seed.py

Revision ID: 373f1e22aeb4
Revises: 0bd7c7cca656
Create Date: 2023-12-18 15:54:45.866483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '373f1e22aeb4'
down_revision: Union[str, None] = '0bd7c7cca656'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            'tipouser',
            sa.column('id', sa.Integer),
            sa.column('tipo', sa.String),
        ),
        [
            {'id': 1, 'tipo': 'Administrador'},
            {'id': 2, 'tipo': 'Cliente'},
        ],
    )


def downgrade() -> None:
    op.execute('DELETE FROM tipouser')
