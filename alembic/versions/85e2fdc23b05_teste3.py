"""teste3

Revision ID: 85e2fdc23b05
Revises: 73cfae358872
Create Date: 2023-10-08 21:09:19.374251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85e2fdc23b05'
down_revision: Union[str, None] = '73cfae358872'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('areas_usuario_id_fkey', 'areas', type_='foreignkey')
    op.drop_column('areas', 'usuario_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('areas', sa.Column('usuario_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('areas_usuario_id_fkey', 'areas', 'usuario', ['usuario_id'], ['id'])
    # ### end Alembic commands ###