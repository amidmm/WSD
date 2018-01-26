
from Utility import read_file
import json
from DoWSD import run_wsd
import numpy as np

ambs = json.loads(read_file('resources/ambigs2002.json'))
total_true = 0
i = 0
test_set = np.random.choice(ambs, 100)
#test_set = ambs[:100]
for item in test_set:
    i += 1
    answer, ranks = run_wsd(item['example'], True)
    electeds = [answer[key] for key in answer]
    if int(item['id']) in electeds:
        total_true += 1
        print("{}/{} Another success: {}".format(total_true, i, item['id'], item['example']))
    else:
        print("{}/{} Failure: {}".format(total_true, i, item['id']), item['example'])

print(total_true, len(test_set))

