from pymongo import MongoClient

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
            if i == 50:
                return self.content
        return self.content

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

#""""""""""""""""""
# LIBS
#""""""""""""""""""

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
        data["img"] = DOMA + "no.png"
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
                m = cleantext(m)
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
