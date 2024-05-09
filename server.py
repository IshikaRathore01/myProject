# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from connection import setup_database
from crud import create_todo, update_todo, delete_todo, get_todo, get_todo_by_id

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # def do_GET(self):
    #     parsed_path = urlparse(self.path)
    #     if parsed_path.path == '/todos':
    #         todos = get_todo(engine, metadata)
    #         todos_dict = [dict(todo) for todo in todos]  # Convert each row to a dictionary
    #         self._set_headers()
    #         self.wfile.write(json.dumps(todos_dict).encode())  # Serialize the list of dictionaries
    #     else:
    #         self._set_headers(404)
    #         self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/todos':
            todos = get_todo(engine, metadata)
            todos_dict = [dict(todo) for todo in todos]
            self._set_headers()
            self.wfile.write(json.dumps(todos_dict).encode())
        elif parsed_path.path.startswith('/todos/'):
            todo_id = parsed_path.path.split('/')[-1]
            todo = get_todo_by_id(engine, metadata, todo_id)
            if todo:
                todo_dict = dict(todo)
                self._set_headers()
                self.wfile.write(json.dumps(todo_dict).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Todo not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        new_todo = json.loads(post_data)
        create_todo(engine, metadata, new_todo['title'], new_todo['content'])
        self._set_headers(201)
        self.wfile.write(json.dumps({"message": "Todo created successfully"}).encode())

    def do_PUT(self):
      parsed_path = urlparse(self.path)
      if parsed_path.path.startswith('/todos/'):
        user_id = int(parsed_path.path.split('/')[-1])
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        updated_todo = json.loads(put_data)
        update_todo(engine, metadata, user_id, updated_todo['title'], updated_todo['content'])  # Call update_todo instead of updated_todo
        self._set_headers(200)
        self.wfile.write(json.dumps({"message": "Todo updated successfully"}).encode())
      else:
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not found"}).encode())


    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/todos/'):
            user_id = int(parsed_path.path.split('/')[-1])
            delete_todo(engine, metadata, user_id)
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "Todo deleted successfully"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    engine, metadata = setup_database()
    run()
