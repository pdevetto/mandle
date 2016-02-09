import urllib

def cleantext(t):
    m = t.encode("windows-1252", "ignore")
    m = m.decode("utf8", "ignore")
    return m
def clean(chaine):
    return chaine.lower().strip()
def decode(chaine):
    chaine = chaine.replace(u"\u2018", "'").replace(u"\u2019", "'")
    try:
        chaine = unicodedata.normalize('NFKD', chaine).encode('ascii','ignore')
        return chaine
    except:
        return chaine
def remove_accents(input_str):
    try:
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
    except:
        return input_str
def cc(i):
    return decode(clean(remove_accents(i)))

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
