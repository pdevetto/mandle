
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
def nospachar(t):
    u = ""
    for i in range(len(t)):
        if 65 <= ord(t[i]) <= 90 or 97 <= ord(t[i]) <= 122:
            u += t[i].lower()
        elif t[i] in [" ", ".", ",", "-", "_", "/"]:
            u += "_"
    return u
