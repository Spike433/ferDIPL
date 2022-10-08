from General import *
import sys
import collections

def BellmanFord(G,s):
    W=edges(G)
    D={}
    for v in G:
        D[v]={'d':sys.maxsize,'p':None}
    D[s]['d']=0
    for i in range(1,len(D)):
        for e in W:
            if D[e[0]]['d']+W[e]<D[e[1]]['d']:
                D[e[1]]={'d':D[e[0]]['d']+W[e],
                         'p':e[0]}
    for e in W:
        if D[e[0]]['d']+W[e]<D[e[1]]['d']:
            raise Exception('negative cycle')
    return D

def BellmanFordFast(G,s):
    W=edges(G)
    D={}
    for v in G:
        D[v]={'d':sys.maxsize,'p':None}
    D[s]['d']=0
    Q=collections.deque()
    Q.append(s)
    while Q:
        u=Q.popleft()
        for e in W:
            if D[e[0]]['d']+W[e]<D[e[1]]['d']:
                D[e[1]]={'d':D[e[0]]['d']+W[e],
                         'p':e[0]}
                if e[1] not in Q:
                    Q.append(e[1])
    for e in W:
        if D[e[0]]['d']+W[e]<D[e[1]]['d']:
            raise Exception('negative cycle')
    return D

