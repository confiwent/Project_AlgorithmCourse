def Create_Graph(bandwith):
    graph = {}
    for i in range(len(bandwith)):
        nodes = []
        for j in range(len(bandwith)):
            if i == j:
                continue
            if bandwith[i][j] != 0:
                nodes.append(str(j))
        graph[str(i)] = nodes
    return graph

def FindAllPath(graph,start,end):
    path=[]
    stack=[]
    stack.append(start)
    visited=set()
    visited.add(start)
    seen_path={}
    #seen_node=[]
    while (len(stack)>0):
        start=stack[-1]
        nodes=graph[start]
        if start not in seen_path.keys():
            seen_path[start]=[]     
        g=0
        for w in nodes:
            if w not in visited and w not in seen_path[start]:
                g=g+1
                stack.append(w)
                visited.add(w)
                seen_path[start].append(w)
                if w==end:
                    path.append(list(stack))
                    old_pop=stack.pop()
                    visited.remove(old_pop)
                break    
        if g==0:
            old_pop=stack.pop()
            del seen_path[old_pop]
            visited.remove(old_pop)
    return path

def FindLargestBandwith(bandwith):
    final_bandwith = []
    graph = Create_Graph(bandwith)
    for i in range(len(bandwith)):
        max_bandwith = []
        for j in range(len(bandwith)):
            if j == i:
                max_bandwith.append(bandwith[i][j])
                continue
            paths = FindAllPath(graph, str(i), str(j))
            min_bandwith = []
            for path in paths:
                min = bandwith[int(path[0])][int(path[1])]
                for k in range(1, len(path)-1):
                    if bandwith[int(path[k])][int(path[k+1])] < min:
                        min = bandwith[int(path[k])][int(path[k+1])]
                min_bandwith.append(min)
            max_bandwith.append(max(min_bandwith))
        final_bandwith.append(max_bandwith)
    return final_bandwith



