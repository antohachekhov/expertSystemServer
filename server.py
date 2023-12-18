from http.server import HTTPServer, BaseHTTPRequestHandler
from ExpertSytemModel.expertSystem import ExpertSystem
import json


class ExpertSystemServer(ExpertSystem):
    expertSystem = None

    def __init__(self, hostname: str = 'localhost', port: int = 8000):
        self._hostname = hostname
        self._port = port

        self._httpd = None
        self._expertSystem = None

    def start(self):
        self._httpd = HTTPServer((self._hostname, self._port), self.HTTPRequestHandler)
        print('Сервер начинает слушать, кажется))')
        self._httpd.serve_forever()

    class HTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/start':
                ExpertSystemServer.expertSystem = ExpertSystem()
                self.send_response(200)
                self.send_header('Origin', 'http://5.128.245.131/')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST, PUT, PATCH, DELETE")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.end_headers()
                self.wfile.write(b'Hello, world!')
                pass
            elif self.path == '/end':
                # получить результат
                try:
                    answer = ExpertSystemServer.expertSystem.getResult()
                    code = 200
                except Exception as e:
                    code = int(str(e)[:3])
                    answer = str(e)[4:]
                self.send_response(code)
                self.send_header('Content-type', 'application/json; charset=UTF-8')
                self.send_header('Origin', 'http://5.128.245.131/')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST, PUT, PATCH, DELETE")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.end_headers()
                self.wfile.write(answer.encode())
                pass
            else:
                self.send_error(404)

        def do_OPTIONS(self):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
            self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_POST(self):
            if self.path == '/send/question':
                contentLength = int(self.headers['Content-Length'])
                body = self.rfile.read(contentLength)
                request = json.loads(body)
                # ответ на вопрос
                try:
                    answer = ExpertSystemServer.expertSystem.answer(request)
                    code = 200
                except Exception as e:
                    print(str(e))
                    if str(e)[:3].isnumeric():
                        code = int(str(e)[:3])
                        answer = str(e)[4:]
                    else:
                        code = 500
                        answer = str(e)
                if code == 200:
                    self.send_response(200)
                    self.send_header('Origin', 'http://5.128.245.131/')
                    self.send_header('Content-type', 'application/json; charset=UTF-8')
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST, PUT, PATCH, DELETE")
                    self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                    self.end_headers()
                    self.wfile.write(answer.encode())
                else:
                    self.send_error(code, answer)
                pass


        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        # self.wfile.write(b'This is POST request. ')
        # self.wfile.write(b'Received: ')
        # self.wfile.write(body)
