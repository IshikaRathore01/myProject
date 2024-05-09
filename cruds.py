from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
from connection import engine

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('age', Integer)
              )

metadata.create_all(engine)

def create_user(name, age):
    with engine.connect() as conn:
        conn.execute(users.insert().values(name=name, age=age))

def read_users():
    with engine.connect() as conn:
        result = conn.execute(users.select())
        return result.fetchall()

def update_user(user_id, new_name, new_age):
    with engine.connect() as conn:
        conn.execute(users.update().where(users.c.id == user_id).values(name=new_name, age=new_age))

def delete_user(user_id):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))

# Example usage
# create_user("Alice", 30)
# create_user("Bob", 25)

# print("Before update:")
# print(read_users())

# update_user(1, "Alice Snith", 31)

# print("\nAfter update:")
# print(read_users())

# # delete_user(2)

# print("\nAfter delete:")
# print(read_users())
