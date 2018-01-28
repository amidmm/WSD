
from Utility import read_file
import json
from DoWSD import run_wsd
import numpy as np

ambs = json.loads(read_file('resources/ambigs2.json'))
#ambs = json.loads(read_file('resources/certains.json'))
total_true = 0
i = 0
test_set = np.random.choice(ambs, 100)
#test_set = ambs[:100]
baseline = 0
fatals = 0
isolated_syns = 0
for item in test_set:
    i += 1
    all_syns = [str(j) for k in item['words'] for j in item['words'][k]]
    answer, ranks = run_wsd((all_syns, item['words']), True)
    ambig_key = item['ambig_word']
    baseline += 1/len(item['words'][ambig_key])
    if ambig_key not in answer:
        is_all_zero = True
        for k in ranks[ambig_key]:
            if k['rank'] != 0:
                is_all_zero = False
        if is_all_zero:
            isolated_syns += 1
        print("Fatal ERROR: ambig key {} is not in answer".format(ambig_key), item, answer)
        fatals += 1
        continue
    if int(item['id']) == answer[item['ambig_word']]:
        total_true += 1
        print("{}/{} id:{} OK".format(total_true, i, item['id'], item['example']))
    else:
        print("{}/{} on:{} id:{}  :(".format(total_true, i, item['ambig_word'], item['id']), item['example'])

print("Precision:{}  Random baseline:{} isolated:{} fatals:{}".format(total_true/len(test_set), baseline/len(test_set),
                                                                      isolated_syns, fatals))

