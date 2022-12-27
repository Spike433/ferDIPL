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

from abc import ABC

class NodeValue(ABC):
    value=None
    def __init__(self,value):
        self.value=value
    def __lt__(self, other):
        if isinstance(other,NodeValue): return self.value<other.value
        else: return False
    def __le__(self, other):
        if isinstance(other,NodeValue): return self.value<=other.value
        else: return False
    def __gt__(self, other):
        if isinstance(other,NodeValue): return self.value>other.value
        else: return False
    def __ge__(self, other):
        if isinstance(other,NodeValue): return self.value>=other.value
        else: return False
    def __eq__(self, other):
        if isinstance(other,NodeValue): return self.value==other.value
        else: return False
    def __str__(self):
        return '{}'.format(self.value)

class Node:
    value=None
    leftNode=None
    rightNode=None
    def __init__(self,value):
        if isinstance(value,NodeValue): self.value=value
    def insert(self,v):
        if isinstance(v,NodeValue) and self.value is not None:
            if v<self.value:
                if self.leftNode is not None: self.leftNode.insert(v)
                else: self.leftNode=Node(v)
            elif v>self.value:
                if self.rightNode is not None: self.rightNode.insert(v)
                else: self.rightNode=Node(v)
    def query(self,p,v):
        if isinstance(v,NodeValue) and self.value is not None:
            if self.value==v: return (p,self)
            elif self.value>v and self.leftNode is not None: return self.leftNode.query(self,v)
            elif self.value<v and self.rightNode is not None: return self.rightNode.query(self,v)
            else: return (None,None)

class BinaryTree:
    rootNode=None
    def insert(self,v):
        if self.rootNode is None: self.rootNode=Node(v)
        else: self.rootNode.insert(v)
    def query(self,v):
        if self.rootNode is not None: return self.rootNode.query(None,v)[1]
        else: return None
    def remove(self,v):
        if self.rootNode is not None:
            (p,n)=self.rootNode.query(None,v)
            if n is None: raise Exception('{} does not exist in the binary tree'.format(v))
            if n.leftNode is not None:
                p=n
                ps=0
                tn=p.leftNode
                while tn.rightNode is not None:
                    p=tn
                    ps=1
                    tn=p.rightNode
                n.value=tn.value
                if ps==0: p.leftNode=tn.leftNode
                else: p.rightNode=tn.leftNode
            elif n.rightNode is not None:
                p=n
                ps=0
                tn=p.rightNode
                while tn.leftNode is not None:
                    p=tn
                    ps=1
                    tn=p.leftNode
                n.value=tn.value
                if ps==0: p.rightNode=tn.rightNode
                else: p.leftNode=tn.rightNode
            else:
                if p is None: self.rootNode=None
                else:
                    if p.leftNode==n: p.leftNode=None
                    elif p.rightNode==n: p.rightNode=None



from copy import deepcopy
from random import choice
from math import floor,ceil

class BCGraph():
    def __init__(self,nodes:list) -> None:
        self.nodes=nodes
        self.G={n1:{n2:0 for n2 in nodes} for n1 in nodes}
        self.EG=deepcopy(self.G)
    def addEdges(self,edgs:list) -> None:
        for (n1,n2) in edgs:
            self.G[n1][n2]=self.G[n2][n1]=1
    def _genHc(self,HcE:list) -> dict:
        Hc=deepcopy(self.EG)
        for (n1,n2) in HcE:
            Hc[n1][n2]=Hc[n2][n1]=1
        return Hc
    def _genHcE(self,Hc:dict) -> list:
        _Hc=deepcopy(Hc)
        res=[]
        for n1 in _Hc:
            for n2 in _Hc[n1]:
                if _Hc[n1][n2]>0 and _Hc[n2][n1]>0:
                    res.append((n1,n2))
                    _Hc[n1][n2]=_Hc[n2][n1]=0
        return res
    def addEdge(self,n1:chr,n2:chr,m:dict,i:int) -> None:
        m[n1][n2]=m[n2][n1]=i
    def _ae(self,n:chr,m:dict) -> int:
        ta=0
        for n1 in self.nodes:
            if m[n][n1]>0: ta=ta+1
        return ta
    def _hasEdge(self,n1:chr,n2:chr,aem:dict,chkOrig:bool=True) -> bool:
        return (chkOrig and self.G[n1][n2]>0) or aem[n1][n2]>0
    def _checkPair(self,n1:chr,n2:chr,aem:dict) -> bool:
        return self._ae(n1,self.G)+self._ae(n2,self.G)+self._ae(n1,aem)+self._ae(n2,aem)>=len(self.nodes)
    def checkClosure(self,addedgs:dict) -> (bool,list):
        i=1
        aem=deepcopy(self.EG)
        res=True
        errs=[]
        while True:
            k=str(i)
            if k in addedgs.keys():
                edg=addedgs[str(i)]
                (n1,n2)=edg
                if self.G[n1][n2]>0:
                    res=False
                    errs.append("Dodani brid ({},{}) već postoji u početnom grafu G".format(n1,n2))
                elif aem[n1][n2]>0:
                    res=False
                    errs.append("Dodani brid ({},{}) već ste prije dodali u postupku stvaranja zatvarača".format(n1,n2))
                elif not self._checkPair(n1,n2,aem):
                    res=False
                    errs.append("Brid ({},{}) ne možete dodati u ovom trenutku jer zbroj stupnjeva priležećih vrhova nije >={}".format(n1,n2,len(self.nodes)))
                else:
                    self.addEdge(n1,n2,aem,i)
            else:
                break
            i=i+1
        for n1 in self.G:
            for n2 in self.G[n1]:
                if n1!=n2 and not self._hasEdge(n1,n2,aem) and self._checkPair(n1,n2,aem):
                    res=False
                    errs.append("Dodanim bridovima još niste stvorili zatvarač G'. Još uvijek možete dodavati bridove, npr. ({},{})!".format(n1,n2))
                    return (res,errs)
        if res:
            self.closure=aem
        return (res,errs)
    def checkHc(self,cHcE:list,tHcE:list) -> (bool,list):
        cHc=self._genHc(cHcE)
        tHc=self._genHc(tHcE)
        res=True
        errs=[]
        for n in tHc:
            if self._ae(n,tHc)!=2:
                res=False
                errs.append("Vrh {} u vašem Hamiltonovom ciklusu nema točno dva priležeća brida!".format(n))
        for (n1,n2) in tHcE:
            if cHc[n1][n2]==0 or cHc[n2][n1]==0:
                res=False
                errs.append("Brid ({},{}) u vašem Hamiltonovom ciklusu ne postoji u ispravnom i očekivanom Hamiltonovom ciklusu!".format(n1,n2))
            cHc[n1][n2]=cHc[n2][n1]=0
        for n1 in cHc:
            for n2 in cHc[n1]:
                if cHc[n1][n2]>0 or cHc[n2][n1]>0:
                    res=False
                    errs.append("U vašem Hamiltonovom ciklusu ne postoji brid koji postoji u ispravnom i očekivanom Hamiltonovom ciklusu, npr. ({},{})".format(n1,n2))
                    return (res,errs)
        return (res,errs)
    def bckStep(self,step:int,change:dict,HcE:list) -> (bool,list,list):
        (u,v)=change["uv"]
        (p,q)=change["pq"]
        Hc=self._genHc(HcE)
        res,errs=True,[]
        for n in Hc:
            if self._ae(n,Hc)!=2:
                res=False
                errs.append("Vrh {} u trenutnom Hamiltonovom ciklusu nema točno dva priležeća brida!".format(n))
        m,n=-1,{(u,v):-1,(p,q):-1}
        for n1 in Hc:
            for n2 in Hc[n1]:
                if Hc[n1][n2]>0 or Hc[n2][n1]>0:
                    if self.closure[n1][n2]>0 and m<self.closure[n1][n2]: m=self.closure[n1][n2]
                    elif self.G[n1][n2]>0 and m<0: m=0
                    for (v1,v2) in [(u,v),(p,q)]:
                        if (v1,v2)==(n1,n2) or (v1,v2)==(n2,n1):
                            if self.closure[v1][v2]>0: n[(v1,v2)]=self.closure[v1][v2]
                            elif self.G[v1][v2]>0: n[(v1,v2)]=0
        maxch=False
        for (n1,n2) in n:
            if n[(n1,n2)]<0:
                res=False
                errs.append("Korak {}: Brid ({},{}) kojeg uklanjate nije dio trenutnog Hamiltonovog ciklusa!".format(step,n1,n2))
            if m==n[(n1,n2)]: maxch=True
        if not maxch:
            res=False
            errs.append("Korak {}: Maksimalni redni broj nadodanog brida u Hamiltonovom ciklusu je {}. Bridovi (u,v)=({},{}) i (p,q)=({},{}) niti jedan nema taj redni broj!".format(step,m,u,v,p,q))
        if self.closure[u][p]>0: n[(u,p)]=self.closure[u][p]
        elif self.G[u][p]>0: n[(u,p)]=0
        if self.closure[v][q]>0: n[(v,q)]=self.closure[v][q]
        elif self.G[v][q]>0: n[(v,q)]=0
        if not self._hasEdge(u,p,self.closure):
            res=False
            errs.append("Korak {}: Brid (u,p)=({},{}) ne postoji u zatvaraču G'".format(step,u,p))
        if self._hasEdge(u,p,Hc,False):
            res=False
            errs.append("Korak {}: Brid (u,p)=({},{}) već postoji u trenutnom Hamiltonovom ciklusu'".format(step,u,p))
        if m<=n[(u,p)]:
            res=False
            errs.append("Korak {}: Brid (u,p)=({},{}) je nadodani i ima viši redni broj ({}) od maksimalno nadodanog brida u trenutnom Hamiltonovom ciklusu ({})'".format(step,u,p,n[(u,p)],m))
        if not self._hasEdge(v,q,self.closure):
            res=False
            errs.append("Korak {}: Brid (v,q)=({},{}) ne postoji u zatvaraču G'".format(step,v,q))
        if self._hasEdge(v,q,Hc,False):
            res=False
            errs.append("Korak {}: Brid (v,q)=({},{}) već postoji u trenutnom Hamiltonovom ciklusu'".format(step,v,q))
        if m<=n[(v,q)]:
            res=False
            errs.append("Korak {}: Brid (v,q)=({},{}) je nadodani i ima viši redni broj ({}) od maksimalno nadodanog brida u trenutnom Hamiltonovom ciklusu ({})'".format(step,v,q,n[(v,q)],m))
        nHcE=None
        if res:
            nHc=deepcopy(Hc)
            nHc[u][v]=nHc[v][u]=0
            nHc[p][q]=nHc[q][p]=0
            nHc[u][p]=nHc[p][u]=1
            nHc[v][q]=nHc[q][v]=1
            nHcE=self._genHcE(nHc)
        return (res,errs,nHcE)
    def isHc(self,HcE:list,chkOrig:bool) -> (bool,list):
        Hc=self._genHc(HcE)
        res,errs=True,[]
        for n in Hc:
            if self._ae(n,Hc)!=2:
                res=False
                errs.append("Vrh {} u trenutnom Hamiltonovom ciklusu nema točno dva priležeća brida!".format(n))
        if chkOrig:
            epairs=[]
            for n1 in Hc:
                for n2 in Hc[n1]:
                    if (n1,n2) not in epairs and Hc[n1][n2]>0 and self.G[n1][n2]==0:
                        epairs.append((n1,n2))
                        epairs.append((n2,n1))
                        res=False
                        errs.append("Brid vašeg Hamiltonovog ciklusa ({},{}) nije sadržan u originalnom grafu!".format(n1,n2))
        start=self.nodes[0]
        self._recIsHc(start,Hc)
        for n1 in Hc:
            for n2 in Hc[n1]:
                if Hc[n1][n2]!=0:
                    res=False
                    errs.append("U slijedu bridova koji ste predali kao Hamiltonov ciklus imate više od jednog ciklusa. Ciklus koji uključuje vrh {} ne sadrži brid ({},{})!".format(start,n1,n2))
        return (res,errs)
    def _recIsHc(self,cn:chr,Hc:dict):
        for an in Hc[cn]:
            if Hc[cn][an]>0:
                Hc[cn][an]=Hc[an][cn]=0
                self._recIsHc(an,Hc)

#bc=BCGraph(['A','B','C','D','E','F','G'])

#bc.addEdges([('A','B'),('A','C'),('A','E'),('B','D'),('B','F'),('B','G'),('C','D'),('D','G'),('E','F'),('E','G')])

#(res,errs)=bc.checkClosure({"1":('B','E'),"2":('B','C'),"3":('C','E'),"4":('C','G'),"5":('C','F'),"6":('D','E'),
#                            "7":('D','F'),"8":('D','A'),"9":('A','F'),"10":('F','G'),"11":('A','G')})
#if not res:
#    for e in errs: print(e)
#else:
#    print("Closure is OK")

#myHC=[('A','B'),('B','C'),('C','D'),('C','E'),('E','F'),('F','G'),('G','A')]
#myHC=[('A','B'),('B','C'),('C','D'),('D','E'),('E','F'),('F','G'),('G','A')]
#(res,errs)=bc.isHc(myHC,False)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Initial HC is correct")

#(res,errs,myHC)=bc.bckStep(1,{"uv":('G','A'),"pq":('B','C')},myHC)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Step 1 is correct: {}".format(myHC))

#(res,errs,myHC)=bc.bckStep(2,{"uv":('F','G'),"pq":('D','E')},myHC)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Step 2 is correct: {}".format(myHC))

#(res,errs,myHC)=bc.bckStep(3,{"uv":('D','F'),"pq":('G','B')},myHC)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Step 3 is correct: {}".format(myHC))

#(res,errs)=bc.isHc(myHC,True)
#if not res:
#    for e in errs: print(e)
#else:
#    print("HC is correct: {}".format(myHC))
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



from random import randint
from math import ceil,floor

# Rabin Karp Algorithm
def rk(pat, txt, q = 101, d = 256):
	M,N,i,j,p,t,h = len(pat),len(txt),0,0,0,0,1
	res = []
	for i in range(M-1):
		h = (h*d)%q
	for i in range(M):
		p = (d*p + ord(pat[i]))%q
		t = (d*t + ord(txt[i]))%q
	for i in range(N-M+1):
		if p==t:
			for j in range(M):
				if txt[i+j] != pat[j]:
					break
				else: j+=1
			if j==M:
				res.append(i)
		if i < N-M:
			t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q
			if t < 0:
				t = t+q
	return res

def searchString(D:list, L:list, Ld:int=4) -> (int, int):
	for j in range(len(L),0,-1):
		r1=rk(L[0:j],D+L)
		r2=list(filter(lambda x: x<Ld, r1))
		if len(r2)>0:
			i=(Ld-1)-max(r2)
			return (i,j)
	return (-1,-1)


def LZ77Encode(I:str, Ld:int=4, La:int=4) -> list:
	# init
	L,I=I[:La],I[La:]
	D=L[0]*Ld
	res=[]
	res.append(L[0])
	while len(L)>0:
		(i,j)=searchString(D,L,Ld)
		if i==-1:
			i,j,k=0,0,L[0]
		else:
			if j==len(L): j,k=j-1,L[-1]
			else: k=L[j]
		res.append((i,j,k))
		T=D+L+I
		D=T[j+1:j+1+Ld]
		L=T[j+1+Ld:j+1+Ld+La]
		I=T[j+1+Ld+La:]
	return res

def LZ77Decode(E:list, Ld:int=4, La:int=4) -> str:
	D,L,res=E[0]*Ld,"",""
	for (i,j,k) in E[1:]:
		B=D+L
		so=j/(i+1)
		t=B[Ld-(i+1):Ld-(i+1)+j]
		W=t
		if so>1:
			for z in range(floor(so-1)): W+=t
			rest=j%(i+1)
			for z in range(rest): W+=t[z]
		W+=k
		res+=W
		B+=W
		D,L=B[len(W):Ld+len(W)],""
	return res

def generateTest() -> str:
	names=["Dalibor","Mihael","Mario","Sonja","Tomislav","Vedran","Kreso"]
	total=randint(10,20)
	res=""
	for i in range(total):
		s1=names[randint(0,len(names)-1)]
		inc=True if randint(0,1)==1 else False
		if inc:
			s2=names[randint(0,len(names)-1)]
			j=randint(0,len(s1)-1)
			s1=s1[:j]+s2+s1[j:]
		res+=s1
	return res

def testCompressedSequence(r:list) -> (bool,list):
	rb,rl=True,[]
	if type(r[0])!=str:
		rb=False
		rl.append("First element must be a character")
	i=1
	for trip in r[1:]:
		if type(trip)!=tuple or len(trip)!=3:
			rb=False
			rl.append("List element {} is not a triplet".format(i))
		else:
			if type(trip[0])!=int:
				rb=False
				rl.append("Triplet {}, element i is not a number".format(i))
			if type(trip[1])!=int:
				rb=False
				rl.append("Triplet {}, element j is not a number".format(i))
			if type(trip[2])!=str:
				rb=False
				rl.append("Triplet {}, element k is not a string".format(i))
		i+=1
	return (rb,rl)
import random

class SkipNode:
    ptrs,v,pred=None,None,None
    def __init__(self,v,p=None,s=None):
        self.v=v
        self.ptrs=[None]
        if p is not None:
            p.ptrs[0]=self
            self.pred=p
        if s is not None:
            self.ptrs[0]=s
            s.pred=self

class SkipList:
    head=SkipNode(None)
    p=0.5
    def __init__(self,p=0.5):
        self.p=p
    def search(self,v):
        n=self._search(v)
        if n.v==v: return n
        else: return None
    def _search(self,v):
        n=self.head
        l=len(n.ptrs)-1
        while l>=0:
            nn=n.ptrs[l]
            if nn is None or nn.v>v:
                l=l-1
            else:
                n=nn
        return n
    def insert(self,v):
        pred=self._search(v)
        s=pred.ptrs[0]
        nn=SkipNode(v,p=pred,s=s)
        x,k=1,len(self.head.ptrs)-1
        while True:
            ctoss=random.uniform(0,1)
            if ctoss<=self.p:
                nn.ptrs.append(None)
                while (len(pred.ptrs)-1)<x and pred is not self.head:
                    pred=pred.pred
                if pred==self.head and x>k:
                    self.head.ptrs.append(None)
                nn.ptrs[x]=pred.ptrs[x]
                pred.ptrs[x]=nn
                x=x+1
            else: break
    def remove(self,v):
        n=self.search(v)
        while n is not None:
            x,pred=0,n.pred
            while (len(n.ptrs)-1)>=x:
                while (len(pred.ptrs)-1)<x and pred is not self.head:
                    pred=pred.pred
                pred.ptrs[x]=n.ptrs[x]
                x=x+1
            n=self.search(v)

