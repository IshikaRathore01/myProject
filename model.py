from sqlalchemy import Column, String,Text ,Enum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from connection import engine
import uuid
from datetime import datetime

Base = declarative_base()
  
class Sources(Base):
    __tablename__ = 'sources'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    sourceName = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    role_id = Column(String, ForeignKey('roles.id'), nullable=False)
    role = relationship("Roles", backref="sources")
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
class Skills(Base):
    __tablename__= 'skills'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    skillName = Column(String(100), nullable=False)
    LEVEL_CHOICES = Enum('Beginner', 'Intermediate', 'Advanced', name='skill_levels')
    level = Column(LEVEL_CHOICES, nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

class Questions(Base):
    __tablename__= 'questions'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    skill_id = Column(String, ForeignKey('skills.id'), nullable=False)
    skill = relationship("Skills", backref="questions")
    source_id = Column(String, ForeignKey('sources.id'), nullable=False)
    source = relationship("Sources", backref="questions")
    question = Column(Text, nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

class Answers(Base):
    __tablename__= 'answers'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    question_id = Column(String, ForeignKey('questions.id'), nullable=False)
    question = relationship("Questions", backref="answers")
    source_id = Column(String, ForeignKey('sources.id'), nullable=False)
    source = relationship("Sources", backref="answers")
    answer = Column(Text, nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

class AnswerCorrectness(Base):
    __tablename__= 'answerCorrectness'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    answer_id = Column(String, ForeignKey('answers.id'), nullable=False)
    answer = relationship("Answers", backref="answerCorrectness")
    source_id = Column(String, ForeignKey('sources.id'), nullable=False)
    reviewed_by = Column(String, ForeignKey('sources.id'))
    source = relationship("Sources", backref="answerCorrectness")
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

class Roles(Base):
    __tablename__= 'roles'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    ROLE_CHOICES = Enum('1', '2', '3', name='role_choice')
    role = Column(ROLE_CHOICES, nullable=False)
    



Base.metadata.create_all(engine)