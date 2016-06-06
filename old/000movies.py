# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os, json, gzip, sys, urllib
from pprint import pprint
from urllib import parse, request

key = "tfhkd9nfhsn5sqysxvxt7c7y"

keydb = "7018dd82b49e527809c9ac486f69223c"

def rottcall(req):
    url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey="
    req = req.replace(' ', '+')
    urlf = url + key + "&q=" + req + "&page_limit=1"
    response = urllib2.urlopen(urlf)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    #print data
    obj = json.loads(data)
    if(len(obj["movies"]) == 1):
        film = obj["movies"][0]
    elif(len(obj["movies"]) == 0):
        c = str(raw_input("Enter a new title for the film to search : "))
        return rottcall(c)
    else:
        print( obj)
        for a in obj["movies"]:
            print( a["title"])
        c = int(raw_input("Enter a Number: "))
        film = obj["movies"][c]
    year = film["year"]
    titl = film["title"]
    real = get_director(film["id"])
    newname = real + " -(" + str(year) + ")- " + titl
    print( " == " +newname+ " == ")
    return newname
    print( "Finish")

def get_director(idfi):
    url = "http://api.rottentomatoes.com/api/public/v1.0/movies/"+idfi+".json?apikey="+key
    response = urllib.request.urlopen(url)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    #print( data)
    obj = json.loads(data)
    if "abridged_directors" in obj:
        if len( obj['abridged_directors'] ) == 1:
            return obj['abridged_directors'][0]['name']
        else:
            for a in obj['abridged_directors']:
                print( a)
            real = str(raw_input("Enter a name for the real : "))
            return real
    else:
        print( "alors")
        pprint(obj)
        real = str(raw_input("Enter a name for the real : "))
        return real

def cleantext(t):
    m = t.encode("windows-1252", "ignore")
    m = m.decode("utf8", "ignore")
    return m

"""
    Faire appel a themoviedb
    Retourne un resultat ou false
"""
def dbcall(req):
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

def dbdir(id):
    params = {'api_key':keydb, 'language' : 'fr'}
    query = urllib.parse.urlencode(params)
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "/credits?" + query

    headers = { 'Accept': 'application/json' }
    request = urllib2.Request(url, headers=headers)
    #print( url)
    response_body =  urllib2.urlopen(request).read()
    #print( response_body)
    data = json.loads(response_body)
    #print( data)
    dir = []
    for i in data['crew'] :
        if i['job'] == 'Director':
            print( i['name'])
            d = i['name'].split(' ')
            dir.append([d[-1], ' '.join(d[0:-1])])

    if len(dir) == 0:
        return
    if len(dir) == 1:
        return dir[0][0] + ', ' + dir[0][1]
    if len(dir) == 2 and dir[0][0] == dir[1][0]:
        return  dir[0][0] + ', ' + dir[0][1] + " & " + dir[1][1]
    return ' and '.join([i[0] + ', ' + i[1] for i in dir])


mp = "/home/pdevetto/Misc/TOKEY"
for name in os.listdir(mp):
    if name.endswith(".avi") or name.endswith(".mkv") or name.endswith(".flv") or name.endswith(".mp4"):
        print( "*********************************\n")
        name2 = name
        for i in ['-', '(',')','.','_','[',']']:
            name2 = name2.replace(i, ' ')
        name3 = name2[:-4].split('(')[0]
        print( name3)
        #dirname = rottcall(name3)
        dirname = ""
        try:
            data = dbcall(name3)

            if not not data :
                if data['empty'] :
                    dirname = "-("+ data['year'] +")- " + name3
                else:
                    real = dbdir(data['id'])
                    dirname = real + " -(" + data['year'] + ")- " + data['title']
                dirname = dirname.replace(":", "-")
                print( ">>>>>>>" + dirname)
                try:
                    os.makedirs(dirname)
                    os.rename(name, dirname+"\\"+name)
                except Exception as inst:
                    print( inst)
                    print( "Probleme de rename : " + name + " > " + dirname+"\\"+name)
            else:
                #a = raw_input("NO DATA")
                print( "no data")
        except Exception as inst:
            print( inst)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print((exc_type, fname, exc_tb.tb_lineno))
