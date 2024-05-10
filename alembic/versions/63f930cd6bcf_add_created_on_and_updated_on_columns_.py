"""Add created_on and updated_on columns to Answers table

Revision ID: 63f930cd6bcf
Revises: a97f97bf617c
Create Date: 2024-05-10 11:21:28.315016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63f930cd6bcf'
down_revision: Union[str, None] = 'a97f97bf617c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.add_column('answers', sa.Column('updated_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answers', 'updated_on')
    op.drop_column('answers', 'created_on')
    # ### end Alembic commands ###