def DFSpaths(graph, start, goals):
    stack = [(start, [start])]
    i = 0
    while stack:
        #if(i>2):break
        (vertex, path) = stack.pop()
        s = set()
        for item in graph.edges([vertex]):
            s.add(item[1])
        for next in s - set(path):
            if next in goals:
                i +=1
                yield path + [next]
            elif len(path) < 2:
                stack.append((next, path + [next]))
