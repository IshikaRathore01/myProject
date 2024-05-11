from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker
from model import Skills,Roles

def get_skills(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Skills).all()
    
def get_roles(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Roles).all()