import MySQLdb
import re
port = 6060
host = 'localhost'

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


def AccuFetchSynset(w,tag):
    import json, os
    filePath = "Resource//synsets.json"
    if not os.path.isfile(filePath):
        file = open(filePath,"a",encoding="utf-8")
        newEntry = fetch_synsets(w,tag)
        file.write(json.dumps({w+"_"+tag:newEntry},ensure_ascii=False))
        file.close()
        return newEntry
    data = json.loads(open(filePath,encoding="utf-8").read())
    try:
        return data[w+"_"+tag]
    except:
        newEntry = fetch_synsets(w,tag)
        data[w+"_"+tag] = newEntry
        open(filePath,'w',encoding="utf-8").writelines(json.dumps(data,ensure_ascii=False))
        return newEntry




def FetchSynsetServer():
    """
    IMPORTANT : should kill the server via FetchServerKill() when you're done
    :return:
    """
    import socket,json,os
    filePath = "Resource//synsets.json"
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    if not os.path.isfile(filePath):
        file = open(filePath,"a",encoding="utf-8").close()
    else:
        data = json.loads(open(filePath,encoding="utf-8").read())
    while 1:
        conn, addr = s.accept()
        request = conn.recv(4096).decode('utf-8')
        #print("Server[request]: " + request)
        if request == "exit_":
            open(filePath,'w',encoding="utf-8").writelines(json.dumps(data,ensure_ascii=False))
            break
        w,tag = request.split("_")
        try:
            conn.sendall(str(data[w+"_"+tag]).encode('utf-8'))
            #print("Server[reply]: " + str(data[w+"_"+tag]))
        except:
            newEntry = fetch_synsets(w,tag)
            data[w+"_"+tag] = newEntry
            conn.sendall(str(data[w+"_"+tag]).encode('utf-8'))
            #print("Server[reply]: " + str(data[w+"_"+tag]))


def FetchSynsetClient(w,tag):
    import socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(str(w+"_"+tag).encode('utf-8'))
    if w=="exit":
        return
    #print("Client[sent]: " + str(w+"_"+tag))
    result = s.recv(4096).decode("utf-8")
    #print("Client[result]: " + result)

def FetchServerKill():
    FetchSynsetClient("exit","")