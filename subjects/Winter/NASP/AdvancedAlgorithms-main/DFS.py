import collections

def DFSIterative(G):
    vis=[]
    S=collections.deque()
    for u0 in G:
        if u0 not in vis:
            S.append(u0)
            while S:
                u=S.pop()
                if u not in vis:
                    vis.append(u)
                    for v in reversed(
                            G[u]['adj']):
                        if v not in vis:
                            S.append(v)
    return vis

def DFS(G):
    vis=[]
    for u0 in G:
        if u0 not in vis:
            DFS_r(G,u0,vis)
    return vis

def DFS_r(G,u,vis):
    vis.append(u)
    for v in G[u]['adj']:
        if v not in vis:
            DFS_r(G,v,vis)


