from Importer import *
from DFSpaths import *

g = importEFromPaj("C:\\Users\\SAMM\\Downloads\\Telegram Desktop\\synset_relation.paj")
for i in DFSpaths(g,"13260","1"):
    print(i)
