
from Preprocess import remove_stop_words
from hazm import *
from Farsnet import fetch_synsets, fetch_definition
from Navigli import buildGraph
from Importer import importFromPaj
from Utility import tagger, normalizer, stemmer
import re, sys
import networkx as nx

FarsNet = importFromPaj("resources/synset_relation.paj")


def run_wsd(sentence, verbose=False):

    all_syns, candid_syns = extract_synsets(sentence)
    '''teleport_set = {}
    for k in candid_syns:
        if len(candid_syns[k]) == 1:
            teleport_set[candid_syns[k][0]] = 0
    if len(teleport_set) > 0:
        for k in teleport_set:
            teleport_set[k] = 1/len(teleport_set)'''
    g = buildGraph(all_syns, FarsNet)
    #nx.write_gexf(g, '/tmp/10215.gephi')
    if verbose:
        print("{} nodes included in graph".format(len(g.nodes())))
    #ranks_deg = nx.degree_centrality(g)
    #ranks_pr = nx.pagerank(g, personalization=teleport_set)
    ranks_pr = nx.pagerank(g)
    ranks = ranks_pr
    #{k: (ranks_deg.get(k, 0) + ranks_pr.get(k, 0))/2 for k in all_syns}
    elected = {}
    output = {}
    for key in candid_syns:
        max_rank = 0
        output[key] = []
        for syn in candid_syns[key]:
            syn_id = str(syn)
            rank = ranks[syn_id]
            if verbose:
                definition = fetch_definition(syn_id)[0]
                definition['rank'] = rank
                output[key].append(definition)
            if rank > max_rank:
                max_rank = rank
                elected[key] = syn
    if verbose:
        return elected, output
    return elected


def extract_synsets(sentence):
    sentence = normalizer.normalize(sentence)
    sentence = re.sub(r'[^\w\s\u200c]', '', sentence)
    words = word_tokenize(sentence)
    words = remove_stop_words(words)
    tags = tagger.tag(words)
    candid_syns = {}
    all_syns = []
    for (w, tag) in tags:
        syns = fetch_synsets(w, tag)
        if len(syns) == 0:
            root = stemmer.stem(w)
            if root is not "":
                syns = fetch_synsets(root, tag)
        if len(syns) > 0:
            candid_syns[w + '_' + tag] = syns
        for s in syns:
            all_syns.append(str(s))
    return all_syns, candid_syns


if len(sys.argv)>2 and sys.argv[1] == 'sen':
    electeds, candids = run_wsd(sys.argv[2], True)
    print(electeds)
    print(candids)
