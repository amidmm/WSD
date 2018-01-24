
import MySQLdb
import re

db = MySQLdb.connect(host="localhost",  # your host
                     user="root",       # username
                     passwd="12345",     # password
                     db="farsnet")
db.set_character_set('utf8')
cur = db.cursor()

cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

# Tagset of Hazm is not the same as tagset of FarsNet
tag_map = {
    'AJ': 'Adjective',
    'AJe': 'Adjective',
    'N': 'Noun',
    'Ne': 'Noun',
    'V': 'Verb',
    'ADV': 'Adverb',
    'ADVe': 'Adverb'
}


def fetch_synsets(w, tag):
    """ Loads all synset ids of given word having given pos tag.
    tag should be from Hazm tagset"""
    if tag in ['PUNC', 'CONJe', 'RESe', 'DETe', 'Pe', 'DET', 'NUM', 'CL', 'P', 'NUMe', 'RES', 'CONJ', 'PRO', 'POSTP', 'INT']:
        return []
    #if tag not in tag_map:
    #    return []
    pos = tag_map[tag]
    w = re.sub(r'[ی]', 'ي', w)
    query = "SELECT id FROM synset WHERE pos=\"" + pos + "\" and id IN (SELECT synset FROM  sense WHERE  value LIKE  \"" + w + "\")"
    cur.execute(query)

    output = []
    for row in cur.fetchall():
        output.append(row[0])
    return output


def fetch_definition(syn):
    if isinstance(syn, list):
        ids = ",".join(syn)
    else:
        ids = syn
    query = "SELECT id, senses_snapshot, gloss FROM synset WHERE id in (" + ids + ")"
    cur.execute(query)

    output = []
    for row in cur.fetchall():
        output.append({'id': row[0], 'gloss': row[2], 'senses_snapshot': row[1]})
    return output

#v=fetch_synsets('دفتر', 'N')
#print(v)
