# coding: utf8

import threading, os, webbrowser
import xml.etree.ElementTree as ET
import BaseHTTPServer
import SimpleHTTPServer

PORT = 8080
DIRE = "/home/pdevetto/Misc/TOKEY"

def cleantext(t):
    m = t.encode("windows-1252", "ignore")
    m = m.decode("utf8", "ignore")
    return m

class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    content = ""

    def do_GET(self):
        """Handle a post request by returning the square of the number."""
        #length = int(self.headers.getheader('content-length'))
        #data_string = self.rfile.read(length)
        print self.path[1:]
        if os.path.isfile(self.path[1:]):
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        self.content = "Hello World"
        self.content += "<hr>"

        M = Movies()
        self.content += M.getAll()

        self.layout()
        return self.view()

    def layout(self):
        layout = "<html><head>"
        layout += "   <title> Mandle </title>"
        layout += "   <script type='text/javascript' src='core.js'></script>"
        layout += "   <link rel='stylesheet' href='core.css' type='text/css' />"
        layout += "</head><body>"
        layout += "<h1> Mandle </h1>"
        layout += self.content
        layout += "</body></html>"
        self.content = layout

    def view(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.content = cleantext(self.content)
        self.wfile.write(self.content)
        return

class Movies:
    content = ""
    def parcourir(self):
        for root, dirs, files in os.walk(DIRE):
            for curfile in files:
                fi, fe = os.path.splitext(curfile)
                if fe == ".nfo":
                    yield os.path.join(root, curfile)

    def getAll(self):
        self.content = ""
        for mov in self.parcourir():
            inf = self.nfoparse(mov)
            print inf
            self.content += "<div class='movie' id='" + str(inf["id"]) + "'>" + "\r\n"
            self.content += "  <img src='" + inf["img"] + "'/>" + "\r\n"
            self.content += "  <span class='title'>" + inf["title"] + "</span><br>" + "\r\n"
            if "director" in inf:
                self.content += "  <span class='real'>" + ",".join(inf["director"]) + "</span>" + "\r\n"
            self.content += "<span class='year'>(" + str(inf["year"]) + ")</span>" + "\r\n"
            self.content += "</div>" + "\r\n"
            #self.content += show(mov)
        return self.content

    def nfoparse(self, path):
        data = {}
        tree = ET.parse(path)
        root = tree.getroot()

        movielt = root

        data["title"] = movielt.find("title").text
        data["note"] = movielt.find("rating").text
        data["year"] = movielt.find("year").text
        data["path"] = path
        data["id"] = movielt.find("id").text

        # DIrectores
        real = movielt.findall("director")
        if len(real) > 0 and real[0].text != None:
            data["director"] = []
            for r in real:
                data["director"].append( r.text )
        else:
            print "PAS DE REAL POUR " + data["title"]
        print " THUMB OF " + data["title"]

        # Image du film
        th = movielt.findall("thumb")
        if len(th) > 0:
            data["img"] = th[0].text
        else:
            data["img"] = "no.png"
        return data

    def show(self, mov):
        self.content = "<div class='movie'> mov </div>"
        return content

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/' % (PORT))
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
