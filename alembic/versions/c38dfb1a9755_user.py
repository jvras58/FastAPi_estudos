"""User

Revision ID: c38dfb1a9755
Revises: 
Create Date: 2023-10-04 17:19:39.732460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c38dfb1a9755'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('senha', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario')
    # ### end Alembic commands ###
