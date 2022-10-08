import collections
from random import randint,choice

def adj(G,u):
    a=[]
    for v in G[u]:
        if G[u][v]!=0:
            a.append(v)
    return a

def edges(G):
    e={}
    for u in G:
        for v in adj(G,u):
            if not (v,u) in e.keys():
                e[(u,v)]=G[u][v]
    return e

def NewAdjMatrix(G,copy=False):
    am={}
    for u in G:
        am[u]={}
        for v in G[u]:
            if copy:
                am[u][v]=G[u][v]
            else:
                am[u][v]=0
    return am

def CopyAdjMatrix(G):
    return NewAdjMatrix(G,True)

def RevPath(D,d):
    P=[d]
    while D[d]['p']!=None:
        d=D[d]['p']
        P.append(d)
    return P

def RevWFI(P,s,d):
    PR=[d]
    while P[s][d]!=0:
        d=P[s][d]
        PR.append(d)
    return PR

def FindCyclesMatrix(G):
    visited=[]
    cycs=[]
    S=collections.deque()
    for u0 in G:
        if u0 not in visited:
            P=NewAdjMatrix(G)
            FindCyclesMatrix_r(G,P,u0,visited,S,cycs)
    return cycs

def FindCyclesMatrix_r(G,P,u,visited,S,cycs):
    visited.append(u)
    S.append(u)
    n=[]
    for v in G[u]:
        if G[u][v]!=0: n.append(v)
    for v in n:
        if v not in S:
            P[u][v]=P[v][u]=1
            FindCyclesMatrix_r(G,P,v,visited,S,cycs)
        else:
            if P[u][v]!=1: # prevents turning back to the previous vertex in undirected graphs
                c = []
                for vx in reversed(S):
                    c.append(vx)
                    if vx is v:
                        break
                if c not in cycs:
                    cycs.append(c)
    S.pop()

def FindCycleWithWeightsMatrix(G):
    c=FindCyclesMatrix(G)
    E2={}
    E=edges(G)
    if len(c)>0:
        c=c[0]
        cp=[(c[-1],c[0])]
        for i in range(len(c)-1):
            cp.append((c[i],c[i+1]))
        for cpi in cp:
            E2=E2|dict(filter(lambda x:x[0][0] in cpi and x[0][1] in cpi,E.items()))
    return E2

def FindCycles(G):
    visited=[]
    cycs=[]
    S=collections.deque()
    for u0 in G:
        if u0 not in visited:
            FindCycles_r(G,u0,visited,S,cycs)
    return cycs

def FindCycles_r(G,u,visited,S,cycs):
    visited.append(u)
    S.append(u)
    for v in G[u]['adj']:
        if v not in S:
            G[v]['p']=u
            FindCycles_r(G,v,visited,S,cycs)
        else:
            if v is not G[u]['p']: # prevents turning back to the previous vertex in undirected graphs
                c = []
                for vx in reversed(S):
                    c.append(vx)
                    if vx is v:
                        break
                if c not in cycs:
                    cycs.append(c)
    S.pop()

def DetectCycle(G):
    visited=[]
    S=collections.deque()
    for u0 in G:
        if u0 not in visited:
            r=DetectCycle_r(G,u0,visited,S)
            if r: return True
    return False

def DetectCycle_r(G,u,visited,S):
    visited.append(u)
    S.append(u)
    for v in G[u]['adj']:
        if v not in S:
            G[v]['p']=u
            r=DetectCycle_r(G,v,visited,S)
            if r: return True
        else:
            if v is not G[u]['p']: # prevents turning back to the previous vertex in undirected graphs
                return True
    S.pop()
    return False

def MakeSet(F,x):
    if x not in F:
        F[x]={'p':x}
    return F

def Find(F,x):
    while F[x]['p']!=x:
        F[x]['p']=F[F[x]['p']]['p']
        x=F[x]['p']
    return x

def Union(F,x,y):
    x=Find(F,x)
    y=Find(F,y)
    F[x]['p']=y

def MatrixToTable(G):
    GR={}
    for v in G:
        GR[v]={'adj':adj(G,v)}
    return GR

def GenerateRandomMatrix(nodes:list, start:chr) -> dict:
    G={n1:{n2:0 for n2 in nodes} for n1 in nodes}
    svl=nodes.index(start)
    w1=[svl]
    while True:
        clds=randint(1,2)
        while clds+len(w1)>len(nodes): clds=randint(1,2)
        vls=[]
        stop=False
        while not stop:
            for c in range(clds):
                x=svl
                while x==svl or x in vls: x=randint(0,len(nodes)-1)
                vls.append(x)
            checks=0
            for tvl in vls:
                if tvl not in w1: checks=checks+1
            stop=checks==clds
            for tvl in vls:
                if G[nodes[svl]][nodes[tvl]]!=0 or G[nodes[tvl]][nodes[svl]]!=0: stop=False
            if not stop: vls.clear()
        if len(w1)>1:
            stop=False
            while not stop:
                s1=svl
                while s1==svl:
                    s1,t1=choice(w1),choice(vls)
                if G[nodes[s1]][nodes[t1]]==0 and G[nodes[t1]][nodes[s1]]==0: stop=True
            w=randint(-10,20)
            if w==0: w=21
            G[nodes[s1]][nodes[t1]]=w
        for tvl in vls:
            w=randint(-10,20)
            if w==0: w=21
            G[nodes[svl]][nodes[tvl]]=w
            if tvl not in w1: w1.append(tvl)
        svl=vls[0]
        if len(w1)==len(nodes): return G

def GenerateRandomCompleteUndirectedGraph(nodes:list) -> dict:
    G={n1:{n2:0 for n2 in nodes} for n1 in nodes}
    for u in G:
        for v in G[u]:
            ui,vi=nodes.index(u),nodes.index(v)
            if vi>ui: G[u][v]=G[v][u]=randint(0,20)
    return G

class StringPL:
    def __init__(self, s: str, p: int=0, l: int=None):
        self.s, self.p = s, p
        if l is None: self.l = len(s)
        else: self.l = l
        if self.s is not None and self.p>len(self.s): raise 'cloning position greater than the length of the string'
        if self.s is not None and self.p+self.l>len(self.s): raise 'cloning position+length greater than the length of the string'
    def substring(self) -> (str):
        return self.s[self.p:self.p + self.l]
    def indexSubstring(self, tp:int, tl:int) -> (str):
        return self.s[tp:tp+tl]
    def clone(self, tp:int, tl:int) -> (object):
        if self.s is None: return StringPL(None, 0, 0)
        if tp>len(self.s): raise 'cloning position greater than the length of the string'
        if tp+tl>len(self.s): raise 'cloning position+length greater than the length of the string'
        return StringPL(self.s, tp, tl)
    def __getitem__(self, item):
        if self.s is None: return None
        if isinstance(item, slice):
            return self.s[item.start+self.p:item.stop+self.p]
        else:
            if item>len(self): raise 'item position greater than the length of the string'
            return self.substring()[item]
    def __len__(self):
        return self.l
    def __str__(self):
        return self.substring()
    def __lt__(self, other):
        return self.substring() < other.substring()
    def lcp(self, other):
        l = 0
        ss = self.substring()
        if isinstance(other, str): os = other
        else: os = other.substring()
        for i in range(0, min(len(ss), len(os))):
            if ss[i] == os[i]:
                l = l + 1
            else:
                break
        return l
    def append(self, c: chr):
        self.s = self.s + c
        self.l = self.l + 1
