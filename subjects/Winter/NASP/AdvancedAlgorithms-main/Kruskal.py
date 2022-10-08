from General import *

def KruskalUndirected(G):
    MST=NewAdjMatrix(G)
    E=edges(G)
    E=dict(sorted(E.items(),key=lambda x:x[1]))
    S={}
    for u in G: S=MakeSet(S,u)
    for e in E:
        if Find(S,e[0])!=Find(S,e[1]):
            Union(S,e[0],e[1])
            MST[e[0]][e[1]]=MST[e[1]][e[0]]=E[e]
    return MST


