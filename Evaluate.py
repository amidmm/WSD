
from Utility import read_file, write_file
import json
from DoWSD import run_wsd
import numpy as np


test_set_size = 100
ambs = json.loads(read_file('resources/ambigs2.json'))
#ambs = json.loads(read_file('resources/certains.json'))
test_set = np.random.choice(ambs, test_set_size, False)
#test_set = ambs[:test_set_size]

#write_file('debug/last_test_set2.json', json.dumps(list(test_set), ensure_ascii=False))
#test_set = json.loads(read_file('debug/last_test_set2.json'))

total_true = 0
i = 0
baseline = 0
fatals = 0
isolated_syns = 0
zero_edges = {'positive': 0, 'negative': 0}
sum_edges = 0
sum_nodes = 0
for item in test_set:
    i += 1
    all_syns = [str(j) for k in item['words'] for j in item['words'][k]]
    answer, report = run_wsd((all_syns, item['words']), True, item['id'])
    ranks = report['ranks']
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
    success = int(item['id']) == answer[item['ambig_word']]
    if success:
        total_true += 1
        print("{}/{} id:{} OK".format(total_true, i, item['id'], item['example']))
    else:
        print("{}/{} on:{} id:{}  :(".format(total_true, i, item['ambig_word'], item['id']), item['example'])

    sum_edges += report['edges']
    sum_nodes += report['nodes']
    if report['edges'] == 0:
        if success:
            zero_edges['positive'] += 1
        else:
            zero_edges['negative'] += 1

print("Precision:{}  Random baseline:{} isolated:{} ".format(total_true/test_set_size, baseline/test_set_size,
                                                                      isolated_syns))
print("zero edges:", zero_edges)
print("avg nodes:{} avg edges:{}".format(sum_nodes/test_set_size, sum_edges/test_set_size))
