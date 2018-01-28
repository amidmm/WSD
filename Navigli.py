import networkx as nx
import DFSpaths

def buildGraph(syns,graph):
    g = nx.Graph()
    toverify = []
    for id in syns:
        if id in graph.nodes:
            g.add_node(id,Value=graph.node[id]['Value'])
            toverify.append(id)
    while toverify:
        start = toverify.pop()
        for path in DFSpaths.DFSpaths(graph, start, syns):
            for id in path:
                if id not in syns and id != start:
                    g.add_node(id,Value=graph.node[id]['Value'])
                    syns.append(id)
                    # toverify.append(id)
            for (src, dst) in zip(path, path[1:]):
                try:
                    g.add_edge(src, dst, Relation=graph.edges[(src, dst)]['Relation'])
                except:
                    pass
    return g