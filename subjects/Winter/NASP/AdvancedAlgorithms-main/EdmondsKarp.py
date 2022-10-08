import collections
from General import NewAdjMatrix,MatrixToTable

def BFS(G,s,d):
    vis={}
    Q = collections.deque()
    Q.append(s)
    vis[s]={'p':None}
    while Q:
        u=Q.popleft()
        for v in G[u]['adj']:
            if v not in vis:
                vis[v]={'p':u}
                Q.append(v)
            if v is d: return vis
    return vis

def BFSPath(G,s,d):
    vis=BFS(G,s,d)
    if d not in vis: return []
    v=vis[d]
    path=[d]
    while v['p'] is not None:
        path.insert(0,v['p'])
        v=vis[v['p']]
    if path[0] is not s: return []
    return path

def EdmondsKarp(G,s,d):
    G={'C':G,'F':NewAdjMatrix(G),'Gf':NewAdjMatrix(G,True)}
    p=BFSPath(MatrixToTable(G['Gf']),s,d)
    while len(p)>0:
        cfp=None
        for i in range(0,len(p)-1):
            u=p[i]
            v=p[i+1]
            if cfp is None or cfp>G['Gf'][u][v]:
                cfp=G['Gf'][u][v]
        for i in range(0,len(p)-1):
            u=p[i]
            v=p[i+1]
            f=G['F'][u][v]=G['F'][u][v]+cfp
            G['Gf'][u][v]=G['C'][u][v]-f
            G['Gf'][v][u]=f
        p=BFSPath(MatrixToTable(G['Gf']),s,d)
    fmax=0
    for v in G['C']:
        fmax=fmax+G['F'][s][v]
        fmax=fmax-G['F'][v][s]
    return (fmax,G['F'])



