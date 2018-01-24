import networkx as nx
import DFSpaths

def buildGraph(syns,graph):
    g = nx.Graph()
    toverify = []
    for id in syns:
        if id in graph.nodes:
            g.add_node(id,attr_dict=graph.node[id])
            toverify.append(id)
    while toverify:
        start = toverify.pop()
        for path in DFSpaths.DFSpaths(graph, start, syns):
            for id in path:
                if id not in syns and id != start:
                    g.add_node(id,attr_dict=graph.node[id])
                    syns.append(id)
                    # toverify.append(id)
            for (src, dst) in zip(path, path[1:]):
                try:
                    g.add_edge(src, dst, attr_dict=graph.edges[(src, dst)])
                except:
                    pass
    return g