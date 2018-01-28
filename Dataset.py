import json
import re
from Utility import read_file, tagger, write_file, normalizer, stemmer
from Preprocess import remove_stop_words
from hazm import *
from Farsnet import fetch_synsets
from DoWSD import extract_synsets



def find_ambiguous_examples():
    raw = read_file('resources/farsnetWSDDataset.json')
    parsed_json = json.loads(raw)
    output = json.loads(read_file('resources/FNWords.json'))
    ambigs = json.loads(read_file('resources/ambigs.json'))
    parsed = read_file('parsed_synsets.json')
    parsed = json.loads(parsed)
    for item in parsed_json[:len(parsed)+200]:
        id = int(item['id'])
        if id in parsed:
            continue
        example = normalizer.normalize(item['example'])
        #Remove punctuation, keep halfspace:
        example = re.sub(r'[^\w\s\u200c]', '', example)
        words = word_tokenize(example)
        words = remove_stop_words(words)
        tags = tagger.tag(words)
        synsets = {}
        for (w, tag) in tags:
            syns = fetch_synsets(w, tag)
            if len(syns) == 0:
                root = stemmer.stem(w)
                if root is not "" and root != w:
                    syns = fetch_synsets(root, tag)
            #only save ambigiues words:
            if len(syns) > 0:
                synsets[w + '_' + tag] = syns
                if id in syns:
                    ambigs.append(item)  #this will take the key "words" too, even it is set later
        item['words'] = synsets
        output.append(item)
        parsed.append(id)
        if(len(output) % 10) == 0:
            print("Parsed {} examples, {} ambigs found".format(len(output), len(ambigs)))
    write_file('resources/FNWords.json', json.dumps(output, ensure_ascii=False,))
    write_file('resources/ambigs.json', json.dumps(ambigs, ensure_ascii=False))
    write_file('parsed_synsets.json', json.dumps(parsed, ensure_ascii=False))


def find_ambiguous_examples2():
    raw = read_file('resources/farsnetWSDDataset.json')
    parsed_json = json.loads(raw)
    output = json.loads(read_file('resources/FNWords2.json'))
    ambigs = json.loads(read_file('resources/ambigs2.json'))
    parsed = read_file('parsed_synsets2.json')
    parsed = json.loads(parsed)
    for item in parsed_json[:len(parsed)+2000]:
        id = int(item['id'])
        if id in parsed:
            continue
        example = item['example']
        for sentence in example.split('*'):
            if len(sentence) < 30:
                continue
            entry = item.copy()
            all_syns, candid_syns = extract_synsets(sentence)
            entry['example'] = sentence
            entry['words'] = candid_syns
            for key in candid_syns:
                if id in candid_syns[key] and len(candid_syns[key]) > 1:
                    entry['ambig_word'] = key
                    ambigs.append(entry)
            output.append(entry)
        parsed.append(id)
        if(len(output) % 10) == 0:
            print("Parsed {} examples, {} ambigs found".format(len(output), len(ambigs)))
    write_file('resources/FNWords2.json', json.dumps(output, ensure_ascii=False))
    write_file('resources/ambigs2.json', json.dumps(ambigs, ensure_ascii=False))
    write_file('parsed_synsets2.json', json.dumps(parsed, ensure_ascii=False))

def find_almost_certain_examples():
    """ Tries to find examples in which all words have only one synsets except the main word"""
    ambigs = json.loads(read_file('resources/ambigs2.json'))
    certain_sens = 0
    num_certains = []
    certain_examples = []
    for item in ambigs:
        certain_words = 0
        for key in item['words']:
            if len(item['words'][key]) == 1:
                certain_words += 1
        num_certains.append(certain_words)
        if certain_words == len(item['words'])-1 :
            certain_sens += 1
            certain_examples.append(item)
    import numpy as np
    import matplotlib.pyplot as plt
    print(np.histogram(num_certains))
    plt.hist(num_certains, bins=np.arange(12)-.5)
    plt.ylabel('Probability');
    plt.show()
    print(len(ambigs), certain_sens, sum(num_certains))
    write_file('resources/certains.json', json.dumps(certain_examples, ensure_ascii=False))






#find_almost_certain_examples()
find_ambiguous_examples2()

