from schema import Base

target_metadata = [Base.metadata]


# alembic/versions/001_initial_migration.py

# from alembic import op
# import sqlalchemy as sa

# def upgrade():
#     op.create_table(
#         'users',
#         sa.Column('id', sa.Integer, primary_key=True),
#         sa.Column('name', sa.String),
#         sa.Column('age', sa.Integer)
#     )

# # def downgrade():
# #     op.drop_table('users')
