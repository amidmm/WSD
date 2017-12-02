import networkx as nx


def importEFromPaj(path):
    """
    Import Graph from the paj
    :param path: path of the paj file
    :return: a graph object
    """
    graph = nx.Graph()
    with open(path) as pajFile:
        pajFile.readline()
        for i in pajFile.readlines():
            if i =="*Arcs\n":
                continue
            x=i.split("\"")
            b=x[0].split()
            if len(b)==1:
                graph.add_node(b[0],attr_dict={"Value":x[1]})
            elif len(b)==2:
                graph.add_edge(b[0],b[1],attr_dict={"Relation":x[1]})
                # print(graph.edge[b[0]])
            else :
                pass
    # print("Drawing plot")
    # nx.draw_networkx(graph)
    # print("Done")
    return graph
