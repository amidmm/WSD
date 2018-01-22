
from Preprocess import remove_stop_words
from hazm import *
from Farsnet import fetch_synsets
from Navigli import buildGraph
from Importer import importFromPaj

tagger = POSTagger(model='resources/postagger.model')
FarsNet = importFromPaj("resources/synset_related_to.paj")

def run_wsd(sentence):

    words = word_tokenize(sentence)
    words = remove_stop_words(words)
    tags = tagger.tag(words)
    candid_syns = {}
    all_syns = []
    for (w, tag) in tags:
        syns = fetch_synsets(w, tag)
        candid_syns[w + '_' + tag] = syns
        for s in syns:
            all_syns.append(s)

    g = buildGraph(all_syns, FarsNet)
    return g

run_wsd('انسان معمولا با دوستان صميمي درددل مي کند')