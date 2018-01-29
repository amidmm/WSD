# numpy bug start
#Todo not include in push
import os
os.environ.setdefault('PATH', '')
#numpy buf end 
import networkx as nx
import time

def CsvExport(graph,id=1):
    dir = os.path.dirname("export")
    if not os.path.exists(dir):
        os.makedirs(dir)
    file = open("export/exportNodes_"+str(id)+"_"+str(time.time())+".csv","w+")
    file2 = open("export/exportEdges_"+str(id)+"_"+str(time.time())+".csv","w+")
    file.writelines("Id,Label\n")
    file2.writelines("Source,Target,Relation\n")
    for i in graph.nodes():
        file.writelines(i+",\""+graph.node[i]["Label"]+"\"\n")
    for (i,j) in graph.edges():
        file2.writelines(i+","+j+",\""+graph.edges[i,j]['Relation']+"\"\n")
    file.close()
    file2.close()
