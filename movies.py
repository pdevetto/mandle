import os,  ConfigParser, imp, time, random
import xml.etree.ElementTree as ET
import pidevs
try:
    imp.find_module('pymongo')
    from pymongo import MongoClient
    MONGO = True
except ImportError:
    MONGO = False
try:
    imp.find_module('Levenshtein')
    import Levenshtein
    LEVEN = True
except ImportError:
    LEVEN = False

class Morage:
    movies = 0
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.mandle
        self.movies = db.movies

    def insert(self, inf):
        movie = inf
        mov_id = self.movies.insert_one(movie).inserted_id

    def find(self, mid):
        return self.movies.find_one({"id": mid})

class Movies:
    content = ""
    domain = ""
    MO = 0
    def __init__(self, doma, dire):
        config = ConfigParser.ConfigParser()
        config.read("config.ini")
        self.modir = config.get("mandle",'modir')
        self.domain = doma
        self.MO = Morage()

    """
    Go through all the movies in the directory
    """
    def parcourir(self):
        for root, dirs, files in os.walk(self.modir):
            for curfile in files:
                fi, fe = os.path.splitext(curfile)
                if fe == ".nfo":
                    yield os.path.join(root, curfile)

    """
    Return HTML for the 50 first movies
    """
    def getAll(self):
        self.content = ""
        i = 0
        for mov in self.parcourir():
            inf = self.nfoparse(mov)
            if inf["year"] != None:
                self.content += self.show(inf)
                i += 1
            if i == 50:
                return self.content
        return self.content

    """
    Yield randomly through all the movies in the directory
    """
    def parcourand(self):
        all = []
        start = time.time()
        for root, dirs, files in os.walk(self.modir):
            for curfile in files:
                fi, fe = os.path.splitext(curfile)
                if fe == ".nfo":
                    all += [os.path.join(root, curfile)]
        end = time.time()
        print end - start, " seconds"
        random.shuffle(all)
        for i in all:
            yield i

    """
    Return HTML for 50 randomly choosed movies
    """
    def getRand(self):
        self.content = ""
        i = 0
        for mov in self.parcourand():
            inf = self.nfoparse(mov)
            if inf["year"] != None:
                self.content += self.show(inf)
                i += 1
            if i == 50:
                return self.content
        return self.content

    """
    Search in movie name
    """
    def search(self, sst):
        self.content = ""
        i = 0
        for mov in self.parcourir():
            inf = self.nfoparse(mov)
            if sst.lower() in inf["title"].lower():
                self.content += self.show(inf)
                i += 1
            if i == 50:
                return self.content
        return "<h2> Search : " + sst + " </h2> " + self.content

    """
    Movies by year
    """
    def getYear(self, year):
        self.content = ""
        for mov in self.parcourir():
            inf = self.nfoparse(mov)
            if inf["year"] == year:
                self.content += self.show(inf)

        return "<h2> Year : " + year + " </h2> " + self.content

    """
    Movie info, by id
    """
    def getId(self, mid):
        self.content = ""
        print mid
        inf = self.MO.find(mid)
        print inf
        if inf == None:
            for mov in self.parcourir():
                inf = self.nfoparse(mov)
                if inf["id"] == mid:
                    self.content += self.showfull(inf)
                    return self.content
        else:
            self.content += self.showfull(inf["path"], inf["img"])
            return self.content

        return "-- nothing found --"
    """
    By real
    """
    def getReal(self, real):
        self.content = ""
        self.simi = ""
        for mov in self.parcourir():
            print mov
            inf = self.nfoparse(mov)
            if "director" in inf:
                for di in inf["director"]:
                    if pidevs.nospachar(di) == real:
                        self.content += self.show(inf)
                    elif LEVEN and Levenshtein.distance( pidevs.cleantext(pidevs.nospachar(di)), pidevs.cleantext(real)) < 5:
                        self.simi += " LEV " + pidevs.cleantext(pidevs.nospachar(di)) + " - " + pidevs.cleantext(real) + " = " + Levenshtein.distance(pidevs.cleantext(pidevs.nospachar(di)), pidevs.cleantext(real))
                        self.simi += self.show(inf)
                    else:
                        pass
        html = "<h2> Real : " + real + " </h2> " + self.content
        if LEVEN:
            html += " <hr> <h2> Similaires </h2> " + self.simi
        return html


    """
    Return HTML for a movie
    """
    def show(self, inf):
        content = "<div class='movie' id='" + str(inf["id"]) + "'>" + "\r\n"
        content += " <a href='" + self.domain + "id/" + str(inf["id"])  + "'><img src='" + inf["img"] + "'/></a>" + "\r\n"
        content += "  <span class='title'>" + inf["title"] + "</span><br>" + "\r\n"
        if "director" in inf:
            dis = []
            for sho, di in inf["director"].items():
                dis.append("<a href='" + self.domain + "real/" + sho + "'>" + di + "</a>")
            content += "  <span class='real'>" + ",".join(dis) + "</span>" + "\r\n"
        content += "<span class='year'><a href='" + self.domain + "year/" + str(inf["year"]) + "'>(" + str(inf["year"]) + ")</a></span>" + "\r\n"
        content += "</div>" + "\r\n"
        return content

    def showfull(self, path, img):
        movielt = self.allnfoparse(path)
        content = "<h2> " + movielt.find("title").text
        # original title
        if movielt.find("title").text != movielt.find("originaltitle").text:
            content += " ( org: " + movielt.find("originaltitle").text + " )"
        content += " </h2> "
        # IMG
        content += "<div class='movie'>"
        content += path
        content += "<img src='" + img + "'/>" + "\r\n"

        # Year
        content += "Year: " + movielt.find("year").text + " <br> "
        # Top 250
        t250 = movielt.find("top250").text
        if t250 != 0:
            content += "Top 250: " + t250 + " <br> "
        # Rating
        content += "Rating: " + movielt.find("rating").text + " <br> "
        # Actors
        content +=  "Actors <div id='actors' style='border:1px solid black'>"
        acts = movielt.findall("actor")
        for act in acts:
            content += "<a href='" + self.domain + "actor/" +pidevs.nospachar(act.find("name").text) + "'>" + act.find("name").text + "</a> <br>"
        content +=  "</div>"
        # Credits
        content += "Credits : "
        creds = movielt.findall("director")
        for cred in creds:
            content += "<a href='" + self.domain + "real/" +pidevs.nospachar(cred.text) + "'>" + cred.text + "</a> <br>"
        content += "<hr>"
        creds = movielt.findall("credits")
        for cred in creds:
            content += "<a href='" + self.domain + "real/" +pidevs.nospachar(cred.text) + "'>" + cred.text + "</a> <br>"
        # Genres
        content += "Genre : "
        gens = movielt.findall("genre")
        for gen in gens:
            content += "<a href='" + self.domain + "genre/" +pidevs.nospachar(gen.text) + "'>" + gen.text + "</a> &nbsp; "
        content += "<br>"

        #for elem in movielt:
        #    if elem.tag not in ["title", "actor", "year", "credits", "genre", "rating", "originaltitle", "top250", "director", ""]:
        #        content += elem.tag + " : "
        #        if "text" in elem:
        #            content += elem.text
        #        content += "<br>"

        content += "</div>"
        return content

    #""""""""""""""""""
    # LIBS
    #""""""""""""""""""
    def allnfoparse(self, path):
        data = {}
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            self.content += "ERROR ON PARSE" + path
            return data
        root = tree.getroot()
        return root

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
                sho = pidevs.nospachar(r.text)
                data["director"][sho] = r.text
        # Image du film
        th = movielt.findall("thumb")
        if len(th) > 0:
            data["img"] = th[0].text
        else:
            data["img"] = self.domain + "no.png"

        if self.MO.find(data["id"]) == None:
            self.MO.insert( data )
        return data

"""
    Faire appel a themoviedb
    Retourne un resultat ou false
"""
def dbcall(req, keydb):
    #url = "https://api.themoviedb.org/3/search/movie/language=fr&api_key=" + keydb
    mots = req.split()
    mots2 = []
    for m in mots:
        try:
            int(m)
            break
        except:
            if m.lower() not in ['vo', 'vostfr', 'dvdrip', 'brrip', '720p', '1080p', 'wawa', 'xvid', 'www']:
                m = pidevs.cleantext(m)
                mots2.append(m)
            else:
                break
    print( mots2)

    #req = req.findall(r'[A-Z]+[^A-Z]*', str)

    params = {'api_key':keydb, "query" : ' '.join(mots2), 'language' : 'fr'}
    query = urllib.parse.urlencode(params)
    url = "https://api.themoviedb.org/3/search/movie?" + query

    headers = { 'Accept': 'application/json' }
    request = urllib.request.Request(url, headers=headers)
    #print( url)
    response_body =  urllib.request.urlopen(request).read()
    #print( response_body)
    data = json.loads(response_body)
    #print( data)
    #for i, j in data.items() :
    #    print( i)
    print( " >> " + str(data['total_results']) + " R")

    results = [{'empty':False, 'id':i['id'], 'title':i['original_title'], 'year':str(i['release_date']).split('-')[0].strip()} for i in data['results']]
    results_year = [x for x in results if x['year'] != "" and x['year'] in req]

    if len(results) == 0:
        return False
    if len(results) == 1:
        return results[0]
    if len(results_year) == 1:
        return results_year[0]
    for i,res in enumerate(results):
        print( str(i) + " :  " + res['year'] + " - " +  res['title'] )
    i = raw_input("Which one (x to pass) $ ")
    try:
        return results[int(i)]
    except Exception as inst:
        return False
