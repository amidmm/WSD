
from Preprocess import remove_stop_words
from hazm import *
from Farsnet import fetch_synsets, fetch_definition
from Navigli import buildGraph, buildGraphBasedOnShortest
from Importer import importFromPaj
from Utility import tagger, normalizer, stemmer, read_file, write_file
import re
import sys
import json
import networkx as nx
from networkx import algorithms
from networkx.algorithms.link_analysis import hits_alg


FarsNet = importFromPaj("resources/synset_relation.paj")
#FarsNet = importFromPaj("resources/synset_related_to.paj")
#FarsNet = importFromPaj("resources/synset_hypernyms.paj")

def run_wsd(sentence, verbose=False, exportName=False):
    if isinstance(sentence, str):
        all_syns, candid_syns = extract_synsets(sentence)
    elif isinstance(sentence, tuple):
        (all_syns, candid_syns) = sentence
    teleport_set = {}
    for k in candid_syns:
        if len(candid_syns[k]) == 1:
            teleport_set[candid_syns[k][0]] = 10

    L = 3
    #g = buildGraph(all_syns, FarsNet, L)
    g = buildGraphBasedOnShortest(candid_syns, FarsNet, all_syns)

    if exportName != False:
        nx.write_gexf(g, 'export/' + exportName + '.gexf')
    if verbose:
        print("nodes:{} edges:{} teleport:{}".format(len(g.nodes()), len(g.edges()), len(teleport_set)))

    #ranks_deg = nx.degree_centrality(g)

    ranks_pr = nx.pagerank(g)
    if len(teleport_set) > 0:
        ranks_pr = nx.pagerank(g, personalization=teleport_set)

    #hits = {}
    #try:
    #    hits = hits_alg.hits(g, max_iter=1000)[0]
    #except nx.exception.PowerIterationFailedConvergence:
    #    pass
    #ranks_btw = nx.betweenness_centrality(g)
    #rank_lrc = nx.communicability_betweenness_centrality(g)
    ranks = ranks_pr
    #ranks = {k: (ranks_deg.get(k, 0) + ranks_pr.get(k, 0)) for k in all_syns}
    elected = {}
    ranks_report = {}
    for key in candid_syns:
        max_rank = 0
        ranks_report[key] = []
        for syn in candid_syns[key]:
            syn_id = str(syn)
            if syn_id not in ranks:
                continue
            rank = ranks[syn_id]
            if verbose:
                definition = fetch_definition(syn_id)[0]
                definition['rank'] = rank
                ranks_report[key].append(definition)
            if rank > max_rank:
                max_rank = rank
                elected[key] = syn
    if verbose:
        output = {
            'teleport_size': len(teleport_set),
            'ranks': ranks_report,
            'nodes': len(g.nodes()),
            'edges': len(g.edges())
        }
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
            if root is not "" and root != w:
                syns = fetch_synsets(root, tag)
        if len(syns) > 0:
            candid_syns[w + '_' + tag] = syns
        for s in syns:
            all_syns.append(str(s))
    return all_syns, candid_syns


def find_ambig_by_id(syn_id):
    samples = json.loads(read_file('resources/FNWords2.json'))
    for item in samples:
        if item['id'] == str(syn_id):
            return item

electeds = []
candids = []
if len(sys.argv) > 2:
    if sys.argv[1] == 'sen':
        electeds, report = run_wsd(sys.argv[2], True)
        print(electeds)
        print(report)
    elif sys.argv[1] == 'debug':
        syn_id = sys.argv[2]
        item = find_ambig_by_id(syn_id)
        if item != None:
            all_syns = [str(j) for k in item['words'] for j in item['words'][k]]
            electeds, report = run_wsd((all_syns, item['words']), True, syn_id)
            write_file('debug/' + syn_id + '.json', json.dumps((item['example'], electeds, report), ensure_ascii=False, indent=4))
            from subprocess import call
            call(["code", 'debug/' + syn_id + '.json'])
        else:
            print("synset with id {} not found".format(syn_id))

