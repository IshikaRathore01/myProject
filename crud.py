
from sqlalchemy.orm import sessionmaker
from model import Skills,Roles, Sources,Questions, Answers, AnswerCorrectness
from urllib.request import urlopen


def get_skills(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Skills).all()
    
def get_roles(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
      roles =  session.query(Roles).all()
      roles_dict = [role.__dict__ for role in roles]
      return roles_dict

        
def get_sources(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        sources = session.query(Sources).all()
        # sources_dict = [source.__dict__ for source in sources]
        return sources
    


def get_questions(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Questions).all()
    
# def create_role(engine, role):
#     Session = sessionmaker(bind=engine)
#     with Session() as session:
#         new_role = Roles(role=role)
#         session.add(new_role)
#         session.commit()

def create_skill(engine, metadata, skill_name, level):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_skill = Skills(skillName=skill_name, level=level)
        session.add(new_skill)
        session.commit()
    
def create_source(engine, metadata, source_name, url, role_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        source = Sources(sourceName=source_name, url=url, role_id=role_id)
        session.add(source)
        session.commit()

# def create_question(engine, metadata, skill_id, source_id, question_text):
#     Session = sessionmaker(bind=engine)
#     with Session() as session:
#         new_question = Questions(skill_id=skill_id, source_id=source_id, question=question_text)
#         session.add(new_question)
#         session.commit()

def process_data_to_generate_questions(data):
    # Assuming data is a string containing lines of text
    # Split the data into lines and extract questions
    questions = []
    for line in data.split('\n'):
        if line.strip():  # Ignore empty lines
            questions.append(line.strip())  # Assume each line is a question
    return questions

def create_questions(engine, metadata, skill_id, source_id):
    # Fetch the URL associated with the provided source_id
    Session = sessionmaker(bind=engine)
    with Session() as session:
        source = session.query(Sources).filter_by(id=source_id).first()
        skill = session.query(Skills).filter_by(id=skill_id).first()
        if source and skill:
            url = source.url
            # Fetch data from the URL and process it to generate questions
            data = urlopen(url).read().decode('utf-8')
            # Process data and generate questions
            questions = process_data_to_generate_questions(data)
            # Insert generated questions into the questions table
            for question in questions:
                new_question = Questions(skill_id=skill_id, source_id=source_id, question=question)
                session.add(new_question)
            session.commit()
        else:
            print("Source or skill not found.")


def create_answer(engine, metadata, question_id, source_id, answer):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_answer = Answers(question_id=question_id, source_id=source_id, answer=answer)
        session.add(new_answer)
        session.commit()

def create_answer_correctness(engine, metadata, answer_id, source_id, reviewed_by, role_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        answer_correctness  = AnswerCorrectness(answer_id=answer_id, source_id=source_id, reviewed_by=reviewed_by, role_id=role_id,)
        session.add(answer_correctness)
        session.commit()
 
def delete_role(engine, role_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        role_to_delete = session.query(Roles).filter_by(id=role_id).first()
        if role_to_delete:
          session.delete(role_to_delete)
          session.commit()

def delete_source(engine, source_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        source = session.query(Sources).filter_by(id=source_id).first()
        if source:
            session.delete(source)
            session.commit()
            return True
        return False

def delete_skill(engine, skill_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        skill = session.query(Skills).filter_by(id=skill_id).first()
        if skill:
            session.delete(skill)
            session.commit()
            return True
        return False

def delete_question(engine, question_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).first()
        if question:
            session.delete(question)
            session.commit()
            return True
        return False
    
def update_source(engine, source_id, new_source_name, new_url):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        source = session.query(Sources).filter_by(id=source_id).first()
        if source:
            source.sourceName = new_source_name
            source.url = new_url
            session.commit()
            return True
        return False

def update_skill(engine, skill_id, new_skill_name, new_level):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        skill = session.query(Skills).filter_by(id=skill_id).first()
        if skill:
            skill.skillName = new_skill_name
            skill.level = new_level
            session.commit()
            return True
        return False

def update_question(engine, question_id, new_question_text):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).first()
        if question:
            question.question = new_question_text
            session.commit()
            return True
        return False

def get_role_by_id(engine, role_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        role = session.query(Roles).filter_by(id=role_id).first()
        if role:
            return role
        
def get_role_id_by_source_id(engine, source_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        role = session.query(Sources).filter_by(id=source_id).first()
        if role:
            return role.role_id
        else:
            return None


def source_to_dict(source):
    return {
        'id': source.id,
        'sourceName': source.sourceName,
        'url': source.url,
        'created_on': source.created_on,
        'updated_on': source.updated_on,
        
    }

def skill_to_dict(skill):
    return {
        'id': skill.id,
        'skillName': skill.skillName,
        'level': skill.level,
        'created_on': skill.created_on,
        'updated_on': skill.updated_on,

    }

def question_to_dict(question):
    return {
        'id': question.id,
        'question': question.question,
        # Add more fields as needed
    }

def role_to_dict(role):
    return{
        'id': role.id,
        'role': role.role,
    }

# print(get_role_id_by_source_id(engine ,"76e3d4b8-0588-4aac-be26-c7b21e2e35b2"))
