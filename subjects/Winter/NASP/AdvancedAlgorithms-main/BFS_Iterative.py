import collections

def BFS(G):
    vis=[]
    Q = collections.deque()
    for u0 in G:
        if u0 not in vis:
            Q.append(u0)
            vis.append(u0)
            while Q:
                u=Q.popleft()
                for v in G[u]['adj']:
                    if v not in vis:
                        vis.append(v)
                        Q.append(v)
    return vis


