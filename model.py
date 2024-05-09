from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from connection import engine

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    
Base.metadata.create_all(engine)


