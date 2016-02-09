# -*- coding: utf-8 -*-
import ConfigParser, sys, os, urllib2, json, time, shutil, filecmp
import Levenshtein

config = ConfigParser.ConfigParser()
config.read("config.ini")

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
                pass
                # Rechercher des infos
                # Déplacer
                # Créer le fichier de data




if len(sys.argv) <= 1 :
    print "usage : python mandle.py"
else:
    m = mandle()
    m.run()
