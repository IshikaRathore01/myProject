from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from connection import setup_database
from crud import get_skills, get_roles

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/skills':
            skills = get_skills(engine)
            skills_dict = [skill.__dict__ for skill in skills]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(skills_dict).encode())
        # elif parsed_path.path.startswith('/roles/'):
        #     # Handle GET request for a specific role by ID
        #     role_id = parsed_path.path.split('/')[-1]
        #     role = get_role_by_id(engine, metadata, role_id)
        #     if role:
        #         role_dict = dict(role)
        #         self._set_headers()
        #         self.wfile.write(json.dumps(role_dict).encode())
        #     else:
        #         self._set_headers(404)
        #         self.wfile.write(json.dumps({"error": "Role not found"}).encode())
        if parsed_path.path == '/roles':
            roles = get_roles(engine)
            roles_dict = [role.__dict__ for role in roles]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(roles_dict).encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
    #     new_todo = json.loads(post_data)
    #     create_todo(engine, metadata, new_todo['title'], new_todo['content'])
    #     self._set_headers(201)
    #     self.wfile.write(json.dumps({"message": "Todo created successfully"}).encode())

    # def do_PUT(self):
    #   parsed_path = urlparse(self.path)
    #   if parsed_path.path.startswith('/todos/'):
    #     user_id = int(parsed_path.path.split('/')[-1])
    #     content_length = int(self.headers['Content-Length'])
    #     put_data = self.rfile.read(content_length)
    #     updated_todo = json.loads(put_data)
    #     update_todo(engine, metadata, user_id, updated_todo['title'], updated_todo['content'])  # Call update_todo instead of updated_todo
    #     self._set_headers(200)
    #     self.wfile.write(json.dumps({"message": "Todo updated successfully"}).encode())
    #   else:
    #     self._set_headers(404)
    #     self.wfile.write(json.dumps({"error": "Not found"}).encode())


    # def do_DELETE(self):
    #     parsed_path = urlparse(self.path)
    #     if parsed_path.path.startswith('/todos/'):
    #         user_id = int(parsed_path.path.split('/')[-1])
    #         delete_todo(engine, metadata, user_id)
    #         self._set_headers(200)
    #         self.wfile.write(json.dumps({"message": "Todo deleted successfully"}).encode())
    #     else:
    #         self._set_headers(404)
    #         self.wfile.write(json.dumps({"error": "Not found"}).encode())

    # def _set_headers(self, status_code=200):
    #     self.send_response(status_code)
    #     self.send_header('Content-type', 'application/json')
    #     self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    engine, metadata = setup_database()
    run()