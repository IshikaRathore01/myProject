from connection import engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

def create_todo(engine, metadata, title, content):
    todos = Table('todos', metadata, autoload=True, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.execute(todos.insert().values(title=title, content=content))
        session.commit()

def get_todo(engine, metadata):
    todos = Table('todos', metadata, autoload=True, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        result = session.execute(todos.select())
        return result.fetchall()
    
def get_todo_by_id(engine, metadata, id):
    todos_table = Table('todos', metadata, autoload=True, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        todo = session.query(todos_table).filter(todos_table.c.id == id).first()
        return todo

def update_todo(engine, metadata, id, title, content):
    todos = Table('todos', metadata, autoload=True, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.execute(todos.update().where(todos.c.id == id).values(title=title, content=content))
        session.commit()

def delete_todo(engine, metadata, id):
    todos = Table('todos', metadata, autoload=True, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.execute(todos.delete().where(todos.c.id == id))
        session.commit()
  

# delete_todo(35)
# update_todo(3, "nail extention", "moring yoda and some workout")
# def delete_user(engine, metadata, user_id):
#     users = Table('users', metadata, autoload=True, autoload_with=engine)
#     Session = sessionmaker(bind=engine)
#     with Session() as session:
#         session.execute(users.delete().where(users.c.id == user_id))
#         session.commit()
