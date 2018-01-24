from Importer import *
from Navigli import *
import nltk
import networkx as nx
# import matplotlib as plt
#
# plt.interactive(False)
# g = importFromPaj("C:\\Users\\SAMM\\Downloads\\Telegram Desktop\\synset_relation.paj")
g = importFromNet("C:\\Users\\SAMM\\Desktop\\wordnet3.net")

sen = ["3131","24874"]

# nx.draw_networkx(g,with_labels=False,node_size=30)
h = buildGraph(set(sen),g)
print(len(h))
# nx.draw(h)
print(h.node)
pass
# print(h.adj)
