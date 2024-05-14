from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from sqlalchemy.orm import sessionmaker
from model import Skills, Sources,Questions
from connection import setup_database
from crud import (get_skills, create_source, get_sources, create_questions,create_skill
                  ,get_questions,create_answer,create_answer_correctness,get_role_by_id, 
                  get_role_id_by_source_id, source_to_dict,skill_to_dict, get_roles, role_to_dict,
                  delete_question,delete_role,delete_skill,delete_source)

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

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):


  def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/sources':
            sources = get_sources(engine)
            sources_dict = [source_to_dict(source) for source in sources]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(sources_dict).encode())
        elif parsed_path.path == '/skills':
            skills = get_skills(engine)
            skills_dict = [skill_to_dict(skill) for skill in skills]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(skills_dict).encode())
        elif parsed_path.path == '/questions':
            questions = get_questions(engine)
            questions_dict = [question.__dict__ for question in questions]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(questions_dict).encode())
        elif parsed_path.path == '/roles':
            roles = get_roles(engine)
            roles_dict = [role_to_dict(role) for role in roles]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(roles_dict).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

  def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        new_data = json.loads(post_data)
        if self.path == '/sources':
            create_source(engine, metadata, new_data['sourceName'], new_data['url'], new_data['role_id'])
        elif self.path == '/skills':
            create_skill(engine, metadata, new_data['skillName'], new_data['level'])
        elif self.path == '/questions':
            create_questions(engine, metadata, new_data['skill_id'], new_data['source_id'])
        elif self.path == '/answers':
            create_answer(engine, metadata, new_data['question_id'], new_data['source_id'], new_data['answer'])
        elif self.path == '/answerCorrectness':
            if new_data['source_id'] != new_data['reviewed_by']:
                role_id = get_role_id_by_source_id(engine, new_data['source_id'])
                role = get_role_by_id(engine, role_id)
                if role and role.role != '1':
                    create_answer_correctness(engine, metadata, new_data['answer_id'], new_data['source_id'], new_data['reviewed_by'], new_data['role_id'])
                    #create_answer_correctness(engine, metadata, new_data, new_data['answer_id'], new_data['source_id'], new_data['reviewed_by'], new_data['role_id'])
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid role_id"}).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "creator and reviewer must be different"}).encode()) 
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Data created successfully"}).encode())

  def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        updated_data = json.loads(put_data)
        if self.path.startswith('/sources/'):
            source_id = self.path.split('/')[-1]
            update_source(engine, source_id, updated_data['sourceName'], updated_data['url'])
        elif self.path.startswith('/skills/'):
            skill_id = self.path.split('/')[-1]
            update_skill(engine, skill_id, updated_data['skillName'], updated_data['level'])
        elif self.path.startswith('/questions/'):
            question_id = self.path.split('/')[-1]
            update_question(engine, question_id, updated_data['question'])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Data updated successfully"}).encode())
      
  def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/sources/'):
            source_id = parsed_path.path.split('/')[-1]
            delete_source(engine, source_id)
        elif parsed_path.path.startswith('/skills/'):
            skill_id = parsed_path.path.split('/')[-1]
            delete_skill(engine, skill_id)
        elif parsed_path.path.startswith('/questions/'):
            question_id = parsed_path.path.split('/')[-1]
            delete_question(engine, question_id)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Data deleted successfully"}).encode())

   


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    engine, metadata = setup_database()
    run()