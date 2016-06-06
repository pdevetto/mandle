# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ConfigParser, sys, os, urllib2, json, time, shutil, filecmp, Levenshtein, gzip, urllib
from pprint import pprint
import movies

config = ConfigParser.ConfigParser()
config.read("config.ini")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class mandle:
    def __init__(self):
        self.modir = config.get("mandle",'modir')

    def run(self):
        for fil in os.listdir(self.modir):
            # IS a directory

            if os.path.isdir(self.modir +"/"+ fil):
                # IF exists config file
                if false:
                    pass
                # Else
                else:
                    pass
                    # Créer le fichier de data
            # IS a file (and is a movie)
            else:
                print "File " + fil
                movies.dbcall(fil, config.get("mandle",'keydb'))
                # Rechercher des infos
                # Déplacer
                # Créer le fichier de data


if len(sys.argv) <= 0 :
    print "usage : python mandle.py"
else:
    m = mandle()
    m.run()
