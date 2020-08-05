import socketserver
from srv import MyHandler
import settings



if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + "works")
        httpd.serve_forever(poll_interval=1)

