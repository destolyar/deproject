import settings

import traceback
from errors import MethodNotAllowed
from errors import NotFound
from http.server import SimpleHTTPRequestHandler
from utils import normalize_path
from utils import to_bytes
import random as r


class MyHandler(SimpleHTTPRequestHandler):

    def handle_uploader(self, folder, file_name, open_file, cnt_type):
        file = settings.PROJECT_DIR / folder / file_name
        if not file.exists():
            return self.handle_404()
        with file.open(open_file) as fp:
            fl = fp.read()

        self.respond(fl, content_type=cnt_type)

    def respond(self, message, code=200, content_type="text/plain"):
        message = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(message)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()

        self.wfile.write(message)

    def handle_404(self):
        msg = "Not found"
        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        self.respond(traceback.format_exc(), code=500, content_type="text/plain")

    def do_GET(self):
        path = normalize_path(self.path)
        up_path = path.split("/")[-2]
        print(up_path)
        handlers = {
            "/": [self.handle_root, []],
            "/hello/": [self.handle_hello, []],
            "/number/": [self.handle_number, []],
            f"/img/{up_path}/": [self.handle_uploader, ["images", str(up_path), "rb", "image/png"]],
            "/style/": [self.handle_uploader, ["static/styles", "style.css", "r", "text/css"]],
        }
        try:
            handler, args = handlers[path]
            handler(*args)

        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_root(self):
        return super().do_GET()

    def handle_number(self):
        num = r.randint(1, 10)
        f_answer = ('Your random number is: ' + str(num))

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
