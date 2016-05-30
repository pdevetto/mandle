# coding: utf8
import threading, os, webbrowser
import xml.etree.ElementTree as ET
import urllib, BaseHTTPServer, SimpleHTTPServer, urlparse
import Levenshtein
# Templating
from jinja2 import Environment, FileSystemLoader

import pidevs, movies

PORT = 8080
DIRE = "/home/pdevetto/Misc/TOKEY"
DIRE = "/drives/m/Films/"
DOMA = "http://localhost:%s/" % (PORT)

class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    content = ""
    title = "home"

    def do_GET(self):
        """Handle a post request by returning the square of the number."""
        #length = int(self.headers.getheader('content-length'))
        #data_string = self.rfile.read(length)
        if os.path.isfile(self.path[1:]):
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        M = Movies()

        expl = self.path.split("/")
        print expl
        if expl[1] == "real":
            self.title = "real: " + expl[2]
            self.content += M.getReal(expl[2])
        elif expl[1] == "year":
            self.title = expl[2]
            self.content += M.getYear(expl[2])
        elif expl[1] == "search":
            parsed = urlparse.urlparse(self.path)
            s = urlparse.parse_qs(parsed.query)['s']
            self.title = "search:" + s[0]
            self.content += M.search(s[0])
        else:
            self.content += M.getAll()
        return self.view()

    def view(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        env = Environment(loader=FileSystemLoader('%s' % os.path.dirname(__file__)))
        template = env.get_template('index.htm')
        self.content = template.render(DOMA=DOMA, content=self.content, title=self.title)

        self.content = cleantext(self.content)
        self.wfile.write(self.content)
        return

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open(DOMA)
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    print "Listening on port ", PORT
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    open_browser()
    start_server()
