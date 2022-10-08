from queue import PriorityQueue
from GeomGeneral import Point

class Event(Point):
    def __init__(self,p=None,x=0,y=0):
        if p is not None and isinstance(p,Point): super().__init__(p.x,p.y)
        else: super().__init__(x,y)
    def __lt__(self, other):
        if isinstance(other,Event): return self.y>other.y or (self.y==other.y and self.x<other.x)
        else: raise Exception('type missmatch')
    def __gt__(self, other):
        if isinstance(other,Event): return self.y<other.y or (self.y==other.y and self.x>other.x)
        else: raise Exception('type missmatch')

class NodeValue():
    e,seq,ls=None,None,None
    def __init__(self, e, seq=None, ls=None):
        self.e,self.seq,self.ls=e,seq,ls
    def __lt__(self, other):
        if isinstance(other, NodeValue):
            if self.seq is not None and other.seq is not None and self.ls is not None and other.ls is not None:
                xs,xo=self.ls.finv(other.e),other.ls.finv(other.e)
                return (xs<xo and abs(xs-xo)>1e-03) or (abs(xs-xo)<=1e-03 and self.seq<other.seq)
            else:
                if other.ls is not None: xs,xo=self.ls.finv(other.e),other.ls.finv(other.e)
                else: xs,xo=self.ls.finv(other.e),other.e.x
                return xs<xo and abs(xs-xo)>1e-03
        else: return False
    def __gt__(self, other):
        if isinstance(other, NodeValue):
            if self.seq is not None and other.seq is not None and self.ls is not None and other.ls is not None:
                xs,xo=self.ls.finv(other.e),other.ls.finv(other.e)
                return (xs>xo and abs(xs-xo)>1e-03) or (abs(xs-xo)<=1e-03 and self.seq>other.seq)
            else:
                if other.ls is not None: xs,xo=self.ls.finv(other.e),other.ls.finv(other.e)
                else: xs,xo=self.ls.finv(other.e),other.e.x
                return xs>xo and abs(xs-xo)>1e-03
        else: return False
    def __eq__(self, other):
        if isinstance(other, NodeValue):
            if self.seq is not None and other.seq is not None and self.ls is not None and other.ls is not None:
                xs,xo=self.ls.finv(other.e),other.ls.finv(other.e)
                return abs(xs-xo)<=1e-03 and self.seq==other.seq
            else:
                if other.ls is not None: return self.ls.p1==other.ls.p1 and self.ls.p2==other.ls.p2
                else:
                    xs,xo=self.ls.finv(other.e),other.e.x
                    return abs(xs-xo)<=1e-03
        else: return False
    def __str__(self):
        return '{}'.format(self.ls)

class Node:
    value,leftNode,rightNode,parent=None,None,None,None
    def __init__(self,value,parent):
        if isinstance(value,NodeValue):
            self.value,self.parent=value,parent
    def insert(self,value):
        if isinstance(value,NodeValue) and self.value is not None:
            if value.seq is None or value.ls is None: raise Exception('inserting node must have sequence and line segment')
            if self.value>value:
                if self.leftNode is not None: self.leftNode.insert(value)
                else: self.leftNode=Node(value,self)
            elif self.value<value:
                if self.rightNode is not None: self.rightNode.insert(value)
                else: self.rightNode=Node(value,self)
    def query(self,e,ls=None,res_eq=[],res_lr={'sl':None,'sr':None}):
        if ls is None: nv=NodeValue(e)
        else: nv=NodeValue(e,None,ls)
        if self.value>nv:
            res_lr['sr']=self.value.ls
            if self.leftNode is not None: self.leftNode.query(e,ls=ls,res_eq=res_eq,res_lr=res_lr)
        elif self.value<nv:
            res_lr['sl']=self.value.ls
            if self.rightNode is not None: self.rightNode.query(e,ls=ls,res_eq=res_eq,res_lr=res_lr)
        else:
            if ls is None: res_eq.append(self)
            elif ls==self.value.ls:
                res_eq.append(self)
                return
            if self.leftNode is not None: self.leftNode.query(e,ls=ls,res_eq=res_eq,res_lr=res_lr)
            if self.rightNode is not None: self.rightNode.query(e,ls=ls,res_eq=res_eq,res_lr=res_lr)

class BinaryTree:
    rootNode=None
    def insert(self,e,Se):
        s1=s2=None
        q=[]
        bp=e.y-0.5
        for ls in Se:
            if not ls.isHorizontal() and ls.bottomPoint().y>bp: bp=ls.bottomPoint().y
        for ls in Se:
            if not ls.isHorizontal():
                if s1 is None: s1=ls
                s2=ls
                xh=ls.finv(Point(e.x,bp))
                q.append({'x':xh,'seq':None,'ls':ls})
        q=sorted(q,key=lambda x:x['x'])
        seq=1
        for item in q:
            item['seq']=seq
            seq=seq+1
        for ls in Se:
            if ls.isHorizontal():
                if s1 is None: s1=ls
                s2=ls
                q.append({'x':e.x,'seq':seq,'ls':ls})
                seq=seq+1
        lim=round(len(q)/2)
        for i in range(lim-1,-1,-1):
            nv=NodeValue(e,q[i]['seq'],q[i]['ls'])
            if self.rootNode is not None: self.rootNode.insert(nv)
            else: self.rootNode=Node(nv,None)
        for i in range(lim,len(q)):
            nv=NodeValue(e,q[i]['seq'],q[i]['ls'])
            if self.rootNode is not None: self.rootNode.insert(nv)
            else: self.rootNode=Node(nv,None)
        return (s1,s2)
    def query(self,e,ls=None):
        Le,Ce,Sl,Sr=[],[],None,None
        if self.rootNode is not None:
            res_eq,res_lr=[],{'sl':None,'sr':None}
            self.rootNode.query(e,ls=ls,res_eq=res_eq,res_lr=res_lr)
            Sl,Sr=res_lr['sl'],res_lr['sr']
            for n in res_eq:
                if n.value.ls.isLowerPoint(e): Le.append(n.value.ls)
                if n.value.ls.isInteriorPoint(e): Ce.append(n.value.ls)
        return {'Le':Le,'Ce':Ce,'Sl':Sl,'Sr':Sr}
    def _query(self,e,ls=None):
        res_eq,res_lr=[],{'sl':None,'sr':None}
        self.rootNode.query(e,ls=ls,res_eq=res_eq,res_lr=res_lr)
        if len(res_eq)>0: return res_eq[0]
        return None
    def _remove(self,n):
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
            if tn.leftNode is not None: tn.leftNode.parent=p
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
            if tn.rightNode is not None: tn.rightNode.parent=p
        else:
            if n.parent is None: self.rootNode=None
            else:
                p=n.parent
                if p.leftNode==n: p.leftNode=None
                elif p.rightNode==n: p.rightNode=None
    def remove(self,e,Se):
        for ls in Se:
            n=self._query(e,ls=ls)
            if n is not None: self._remove(n)

def ProcessEvent(e,Q,tau,I,S,SS):
    Ue=[]
    for ls in S:
        if ls.isUpperPoint(e):
            Ue.append(ls)
    tauQuery=tau.query(e)
    Le,Ce=tauQuery['Le'],tauQuery['Ce']
    sl,sr=tauQuery['Sl'],tauQuery['Sr']
    if len(Ue)+len(Le)+len(Ce)>1 and (e.x,e.y) not in I:
        I.append({(e.x,e.y):Le+Ue+Ce})
    tau.remove(e,Le+Ce)
    (s1,s2)=tau.insert(e,Ue+Ce)
    if len(Ue+Ce)==0:
        if sl is not None and sr is not None:
            i=sl.intersection(sr)
            if i is not None and i not in SS:
                Q.put(Event(i))
                SS.add(i)
    else:
        if sl is not None:
            i=s1.intersection(sl)
            if i is not None and i not in SS:
                Q.put(Event(i))
                SS.add(i)
        if sr is not None:
            i=s2.intersection(sr)
            if i is not None and i not in SS:
                Q.put(Event(i))
                SS.add(i)

def PlaneSweepLSIntersection(S):
    Q,SS=PriorityQueue(),set()
    for ls in S:
        Q.put(Event(ls.p1))
        SS.add(ls.p1)
        Q.put(Event(ls.p2))
        SS.add(ls.p2)
    I=[]
    tau=BinaryTree()
    while not Q.empty():
        e=Q.get()
        ProcessEvent(e,Q,tau,I,S,SS)
    return I



