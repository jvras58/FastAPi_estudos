"""coluna_disponibilidade_add_em_reserva

Revision ID: 51dc5387141f
Revises: 85e2fdc23b05
Create Date: 2023-10-09 11:19:51.541904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51dc5387141f'
down_revision: Union[str, None] = '85e2fdc23b05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('disponivel', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservations', 'disponivel')
    # ### end Alembic commands ###
