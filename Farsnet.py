
import MySQLdb

db = MySQLdb.connect(host="localhost",  # your host
                     user="root",       # username
                     passwd="12345",     # password
                     db="farsnet")
db.set_character_set('utf8')
cur = db.cursor()

cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

tag_map = {
'AJ' : 'Adjective',
'N' : 'Noun',
'Ne' : 'Noun',
'V' : 'Verb',
'ADV' : 'Adverb',
}

def fetch_synsets(w, tag):
    pos = tag_map[tag]
    query = "SELECT id FROM synset WHERE pos=\"" + pos + "\" and id IN (SELECT synset FROM  sense WHERE  value LIKE  \"" + w + "\")"
    cur.execute(query)

    output = []
    for row in cur.fetchall():
        output.append(row[0])
    return output


#v=fetch_synsets('دفتر', 'N')
#print(v)