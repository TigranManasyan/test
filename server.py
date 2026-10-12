'''
REST API
REST Respresentational State Transfer 

1. resources - /api/v1/students
2. http - get (select), post (insert), put/patch (update), delete (delete) CRUD
3. stateless - 
4. JSON


'''


from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
import socketserver

class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

students = [
    {"id":1, "name": "Karen", "age": 30, "course": "Development"},
    {"id":2, "name": "Anna", "age": 20, "course": "UI/UX"},
    {"id":3, "name": "Erik", "age": 22, "course": "Java Development"}
]

class RESTReqiestHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response)

    def parse_path(self):
        parsed_url = urlparse(self.path)
        path_parts = [p for p in parsed_url.path.split("/") if p]
        # http://localhost:8000/api/students/1, ['api', 'students', '1']
        if len(path_parts) >= 2 and path_parts[0] == 'api' and path_parts[1] == 'students':
            student_id = int(path_parts[2]) if len(path_parts) == 3 and path_parts[2].isdigit() else None
            return True, student_id
        return False, None

    def get_request_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return None

        body = self.rfile.read(content_length)

        try:
            return json.loads(body.decode('utf-8'))
        except Exception as error:
            print(f"JSON parse error: {error}")
            return None

    def do_GET(self):
        is_valid_route, student_id = self.parse_path()

        if not is_valid_route:
            self.send_json({"error":"Endpoint-ը վավեր չէ"}, 404)
            return 

        if student_id is None:
            self.send_json(students)
            return


        student = next((s for s in students if s['id'] == student_id), None)
        if student:
            self.send_json(student)
        else:
            self.send_json({"error": 'Ուսանողը չի գտնվել'}, 404)

            
    def do_POST(self):
        is_valid_route, student_id = self.parse_path()
        if not is_valid_route or student_id is not None:
            self.send_json({"error": 'Անվավեր URL POST հարցման համար'}, 400)
            return

        body = self.get_request_body()
        if not body or 'name' not in body or 'course' not in body:
            self.send_json({"error": "name և course դաշտերը պարտադիր են"}, 400)
            return 

        new_id = max([s['id'] for s in students], default = 0) + 1
        new_student = {
            "id": new_id,
            "name": body['name'],
            "course": body['course']
        }
        students.append(new_student)
        self.send_json(new_student, 201)

    def do_PUT(self):
        is_valid_route, student_id = self.parse_path()
        if not is_valid_route or student_id is None:
            self.send_json({"error": 'Ուսնաողի id-ին նշված չէ'}, 400)
            return

        student = next((s for s in students if s['id'] == student_id), None)
        if not student:
            self.send_json({"error":"Ուսանողը չի գտնվել"}, 404)
            return

        body = self.get_request_body()
        if not body:
            self.send_json({"error":"Փոխանցված տվյալներ չկան կամ JSON-ը վավաեր չէ"})
            return

        student['name'] = body.get('name', student['name'])
        student['course'] = body.get('course', student['course'])

        self.send_json(student)

    def do_DELETE(self):
        global students
        is_valid_route, student_id = self.parse_path()
        if not is_valid_route or student_id is None:
            self.send_json({"error": 'Ուսնաողի id-ին նշված չէ'}, 400)
            return

        student = next((s for s in students if s['id'] == student_id), None)
        if not student:
            self.send_json({"error":"Ուսանողը չի գտնվել"}, 404)
            return

        students = [s for s in students if s['id'] != student_id]
        self.send({"msg":f"ID {student_id} ուսանողը հաեռացվել է"})

        
def run_server(port=8000):
    server_addr = ('', port)
    httpd = ThreadingHTTPServer(server_addr, RESTReqiestHandler)
    print(f"Սերվերը գործարկվել է https://localhost:{port}/api/students հասցեով")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Սերվերը կանգնեց")

if __name__ == '__main__':
    run_server()