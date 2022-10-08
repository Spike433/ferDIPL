import copy
from collections import deque
from General import MatrixToTable
from BlockSearch import BlockSearch
from WFI import WFI,RevWFI
import sys

def IsEulerianCircuit(G, u):
    hasMore=True
    while hasMore:
        u0=u
        while G[u]['adj']:
            v=G[u]['adj'][0]
            G[u]['adj'].remove(v)
            G[v]['adj'].remove(u)
            u=v
        if u0 is not u:
            return False
        hasMore=False
        for u in G:
            if G[u]['adj']:
                hasMore=True
                break
    return True

def Fleury(G,u):
    cycle=[]
    blocks=BlockSearch(G)
    while G[u]['adj']:
        for v in G[u]['adj']:
            exit=False
            for b in blocks:
                if len(b)>1 and ((u,v) in b or (v,u) in b):
                    exit=True
                    break
            if exit: break
        G[u]['adj'].remove(v)
        G[v]['adj'].remove(u)
        blocks=BlockSearch(G)
        cycle.append((u,v))
        u=v
    return cycle

def Hierholzer(G,u):
    s=deque()
    cycle=[]
    s.append(u)
    while s:
        u=s[-1]
        if len(G[u]['adj'])>0:
            v=G[u]['adj'][0]
            s.append(v)
            G[u]['adj'].remove(v)
            G[v]['adj'].remove(u)
        else:
            if len(s)>1: cycle.append((s[-1],s[-2]))
            s.pop()
    return cycle

def _permutate(l=[]):
    res=[]
    if len(l)>1:
        a=l[0]
        l.remove(a)
        for b in l:
            t=(a,b)
            l2=l.copy()
            l2.remove(b)
            rl=_permutate(l2)
            if len(rl)>0:
                for c in rl:
                    res_tmp=[t]
                    if isinstance(c,list):
                        for d in c: res_tmp.append(d)
                    else: res_tmp.append(c)
                    res.append(res_tmp)
            else:
                res.append([t])
    return res

def Eulerization(G):
    ODD=[]
    for u in G:
        t=list(filter(lambda x: G[u][x]>0,G[u]))
        if len(t)%2!=0: ODD.append(u)
    (D,P)=WFI(copy.deepcopy(G))
    BG=_permutate(ODD.copy())
    M={'r':sys.maxsize}
    for combo in BG:
        tot=0
        for t in combo: tot=tot+D[t[0]][t[1]]
        if tot<M['r']:
            M={'r':tot,'p':{}}
            for t in combo: M['p'][t]=RevWFI(P,t[0],t[1])
    G=MatrixToTable(G)
    for t in M['p']:
        p=M['p'][t]
        while len(p)>=2:
            G[p[0]]['adj'].append(p[1])
            G[p[1]]['adj'].append(p[0])
            del p[0]
    return G
