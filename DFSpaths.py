def DFSpaths(graph, start, goals):
    stack = [(start, [start])]
    i = 0
    while stack:
        #if(i>2):break
        (vertex, path) = stack.pop()
        s = set()
        for item in graph.edge[vertex]:
            s.add(item)
        for next in s - set(path):
            if next in goals:
                i +=1
                yield path + [next]
            elif len(path)<5:
                stack.append((next, path + [next]))
