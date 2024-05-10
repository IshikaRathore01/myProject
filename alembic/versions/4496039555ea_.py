"""empty message

Revision ID: 4496039555ea
Revises: 9796eaa0e02c
Create Date: 2024-05-10 14:35:39.907657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4496039555ea'
down_revision: Union[str, None] = '9796eaa0e02c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answerCorrectness', 'reviewed_by',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answerCorrectness', 'reviewed_by',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
