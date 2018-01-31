import networkx as nx
import DFSpaths

def buildGraph(syns, graph, L):
    g = nx.Graph()
    toverify = []
    for id in sorted(syns):
        if id in graph.nodes:
            g.add_node(id, Value=graph.node[id]['Value'] + ';' + id)
            toverify.append(id)
    while toverify:
        start = toverify.pop()
        for path in DFSpaths.DFSpaths(graph, start, syns, L):
            for id in path:
                if id not in syns and id != start:
                    g.add_node(id, Value=graph.node[id]['Value'] + ';' + id)
                    syns.append(id)
                    # toverify.append(id)
            for (src, dst) in zip(path, path[1:]):
                try:
                    g.add_edge(src, dst, Relation=graph.edges[(src, dst)]['Relation'])
                except:
                    pass
    #if len(g.edges()) == 0 and L < 10:
    #    return buildGraph(syns, graph, L+1)
    return g


def buildGraphBasedOnShortest(candids, graph, flat_syns=False):
    """Builds graph based on shortest path between various words in sentence
    Also has an override that augments navigli graph with shortest paths
    """
    if flat_syns:
        g = buildGraph(flat_syns, graph, 2)
    else:
        g = nx.Graph()

    for base_word in sorted(candids):
        for id in candids[base_word]:
            id = str(id)
            if id not in graph.nodes:
                candids[base_word].pop(id)
            g.add_node(id, Value=graph.node[id]['Value'] + ';' + id)

    for base_word in sorted(candids):
        for other_word in sorted(candids):
            if base_word == other_word:
                continue
            for base_syn in sorted(candids[base_word]):
                source_syn = str(base_syn)
                for other_syn in sorted(candids[other_word]):
                    target_syn = str(other_syn)
                    try:
                        path = nx.shortest_path(graph, source_syn, target_syn)
                        for syn_id in path:
                            g.add_node(id, Value=graph.node[id]['Value'] + ';' + id)
                        try:
                            g.add_path(path)#src, dst, Relation=graph.edges[(src, dst)]['Relation'])
                        except:
                            pass
                    except nx.exception.NetworkXNoPath:
                        pass


    return g

