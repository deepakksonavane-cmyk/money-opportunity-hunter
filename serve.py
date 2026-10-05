from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os

PORT = 8000

os.chdir(os.path.dirname(__file__))

server = ThreadingHTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
print(f"Open http://localhost:{PORT} in your browser")
server.serve_forever()
