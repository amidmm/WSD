import json
import re
from Utility import read_file, tagger, write_file, normalizer, stemmer
from Preprocess import remove_stop_words
from hazm import *
from Farsnet import fetch_synsets


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
                syns = fetch_synsets(root, tag)
            #only save ambigiues words:
            if len(syns) > 1:
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


find_ambiguous_examples()
