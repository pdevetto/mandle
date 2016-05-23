# coding: utf8

import threading, os, webbrowser
import xml.etree.ElementTree as ET
import BaseHTTPServer
import SimpleHTTPServer
#import Levenshtein

PORT = 8080
DIRE = "/home/pdevetto/Misc/TOKEY"
DIRE = "/drives/m/Films/"
DOMA = "http://localhost:%s/" % (PORT)

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
        if os.path.isfile(self.path[1:]):
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        M = Movies()

        expl = self.path.split("/")
        print expl
        if expl[1] == "real":
            self.content += M.getReal(expl[2])
        elif expl[1] == "year":
            self.content += M.getYear(expl[2])
        else:
            self.content += M.getAll()

        self.layout()
        return self.view()

    def layout(self):
        layout = "<html><head>"
        layout += "   <title> Mandle </title>"
        layout += "   <script type='text/javascript' src='" + DOMA + "core.js'></script>"
        layout += "   <link rel='stylesheet' href='" + DOMA + "core.css' type='text/css' />"
        layout += "</head><body>"
        layout += "<h1> Mandle </h1>"
        layout += "<div id='menu'>  <a href='" + DOMA + "'> root </a> </div>"
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

def nospachar(t):
    u = ""
    for i in range(len(t)):
        if 65 <= ord(t[i]) <= 90 or 97 <= ord(t[i]) <= 122:
            u += t[i].lower()
        elif t[i] in [" ", ".", ",", "-", "_", "/"]:
            u += "_"
    return u

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
        i = 0
        for mov in self.parcourir():
            inf = self.nfoparse(mov)
            if inf["year"] != None:
                self.content += self.show(inf)
                i += 1
            if i == 100:
                return self.content
        return self.content

    def getYear(self, year):
        self.content = ""
        for mov in self.parcourir():
            inf = self.nfoparse(mov)
            if inf["year"] == year:
                self.content += self.show(inf)

        return "<h2> Year : " + year + " </h2> " + self.content

    def getReal(self, real):
        self.content = ""
        self.simi = ""
        for mov in self.parcourir():
            print mov
            inf = self.nfoparse(mov)
            if "director" in inf:
                for di in inf["director"]:
                    if nospachar(di) == real:
                        self.content += self.show(inf)
                    #elif Levenshtein.distance(cleantext(nospachar(di)), cleantext(real)) < 5:
                    #    self.simi += " LEV " + cleantext(nospachar(di)) + " - " + cleantext(real) + " = " + Levenshtein.distance(cleantext(nospachar(di)), cleantext(real))
                    #    self.simi += self.show(inf)
                    else:
                        pass
        return "<h2> Real : " + real + " </h2> " + self.content # + " <hr> <h2> Similaires </h2> " + self.simi

    def show(self, inf):
        content = "<div class='movie' id='" + str(inf["id"]) + "'>" + "\r\n"
        content += "  <img src='" + inf["img"] + "'/>" + "\r\n"
        content += "  <span class='title'>" + inf["title"] + "</span><br>" + "\r\n"
        if "director" in inf:
            dis = []
            for sho, di in inf["director"].items():
                dis.append("<a href='" + DOMA + "real/" + sho + "'>" + di + "</a>")
            content += "  <span class='real'>" + ",".join(dis) + "</span>" + "\r\n"
        content += "<span class='year'><a href='" + DOMA + "year/" + str(inf["year"]) + "'>(" + str(inf["year"]) + ")</a></span>" + "\r\n"
        content += "</div>" + "\r\n"
        return content

    def nfoparse(self, path):
        data = {}
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            self.content += "ERROR ON PARSE" + path
            return data
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
            data["director"] = {}
            for r in real:
                sho = nospachar(r.text)
                data["director"][sho] = r.text
        # Image du film
        th = movielt.findall("thumb")
        if len(th) > 0:
            data["img"] = th[0].text
        else:
            data["img"] = "no.png"
        return data

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
