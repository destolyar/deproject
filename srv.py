import settings
from http.server import SimpleHTTPRequestHandler
import random as r


class MyHandler(SimpleHTTPRequestHandler):

    def respond(self, message, code=200, content_type="text/plain"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(message)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(message.encode())

    def handle_404(self):
        msg = "Not found"
        self.respond(msg, code=404, content_type="text/plain")

    def build_path(self):
        result = self.path

        if result[-1] != "/":
            result = f"{result}"
        return result

    def do_GET(self):
        path = self.build_path()
        if path == "/number":
            self.handle_number()
        elif path == "/hello/":
            self.handle_hello()
        elif path == "/":
            self.handle_root()
        else:
            self.handle_404()

    def handle_root(self):
        return super().do_GET()

    def handle_number(self):
        num = r.randint(1, 10)
        f_answer = ('Your random number: ' + str(num))

        self.respond(str(f_answer))

    def handle_hello(self):
        content = """
        <html>
            <head><title>Some title</title></head>
            <body>
                <h1 align="center">Hello</h1>
        </html>
        """

        self.respond(content, code=200, content_type="text/html")
