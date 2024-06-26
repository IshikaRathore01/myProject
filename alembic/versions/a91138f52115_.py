"""empty message

Revision ID: a91138f52115
Revises: 4439c5cf53f4
Create Date: 2024-05-14 12:36:45.918354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a91138f52115'
down_revision: Union[str, None] = '4439c5cf53f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answerCorrectness', sa.Column('role_id', sa.String(), nullable=False))
    op.create_foreign_key(None, 'answerCorrectness', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'answerCorrectness', type_='foreignkey')
    op.drop_column('answerCorrectness', 'role_id')
    # ### end Alembic commands ###
