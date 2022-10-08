from statistics import mean
from math import ceil
from GeomGeneral import LineSegment,Point
from AVL import AVLTree

class Interval:
    v1,v2=None,None
    v1i,v2i=False,False
    def __init__(self,v1i,v1,v2,v2i):
        self.v1i,self.v1,self.v2,self.v2i=v1i,v1,v2,v2i
    def containedIn(self,ls):
        if self.v1 is not None and self.v1>=ls.p1.x and self.v2 is not None and self.v2<=ls.p2.x:
            return True
        return False
    def inside(self,v):
        if (self.v1 is None or self.v1<=v) and (self.v2 is None or v<=self.v2): return True
        return False
    def containsEndpointsOf(self,ls):
        ins=0
        if type(ls) is LineSegment:
            if self.inside(ls.p1.x): ins=ins+1
            if self.inside(ls.p2.x): ins=ins+1
            if self.containedIn(ls) or ls.containedIn(self): ins=ins+2
        if type(ls) is VerticalTreeValue:
            if self.inside(ls.value[0]): ins=ins+1
            if self.inside(ls.value[1]): ins=ins+1
        if type(ls) is Interval:
            if self.inside(ls.v1): ins= ins + 1
            if self.inside(ls.v2): ins= ins + 1
        if type(ls) is tuple:
            if self.inside(ls[0]): ins= ins + 1
            if self.inside(ls[1]): ins= ins + 1
        return ins
    def intersection(self,Iother):
        tmpInt=None
        if type(Iother) is Interval:
            tmpInt=(Iother.v1,Iother.v2);
        elif type(Iother) is VerticalTreeValue:
            tmpInt=(Iother.value[0],Iother.value[1]);
        elif type(Iother) is LineSegment:
            tmpInt=(Iother.p1.x,Iother.p2.x);
        elif type(Iother) is tuple:
            tmpInt=(Iother[0],Iother[1]);
        if tmpInt is not None:
            (ox1,ox2)=tmpInt
            tx1,tx2=self.v1,self.v2
            if (ox1 is not None and tx2 is not None and ox1>tx2) or (ox2 is not None and tx1 is not None and ox2<tx1): return None
            if tx1 is None and ox1 is None: rx1=None
            elif tx1 is None and ox1 is not None: rx1=ox1
            elif tx1 is not None and ox1 is None: rx1=tx1
            else: rx1=max(tx1,ox1)
            if tx2 is None and ox2 is None: rx2=None
            elif tx2 is None and ox2 is not None: rx2=ox2
            elif tx2 is not None and ox2 is None: rx2=tx2
            else: rx2=min(tx2,ox2)
            return Interval(True,rx1,rx2,True)
        else: return None

class VerticalTreeValue:
    value=None
    def __init__(self,I,ls):
        y1,y2=ls.y(I.v1),ls.y(I.v2)
        if ls.dx==0: y1,y2=ls.p1.y,ls.p2.y
        self.value=(y1,y2,ls)
    def __lt__(self, other):
        if isinstance(other,VerticalTreeValue): return self.value[0]<other.value[0]
        else: return False
    def __le__(self, other):
        if isinstance(other,VerticalTreeValue): return self.value[0]<=other.value[0]
        else: return False
    def __gt__(self, other):
        if isinstance(other,VerticalTreeValue): return self.value[0]>other.value[0]
        else: return False
    def __ge__(self, other):
        if isinstance(other,VerticalTreeValue): return self.value[0]>=other.value[0]
        else: return False
    def __eq__(self, other):
        if isinstance(other,VerticalTreeValue): return self.value[0]==other.value[0]
        else: return False
    def __str__(self):
        return '{}'.format(self.value)
    def recalculateY(self,HIq):
        (y1,y2,ls)=self.value
        y1,y2=ls.y(HIq.v1),ls.y(HIq.v2)
        if ls.dx==0: y1,y2=ls.p1.y,ls.p2.y
        return Interval(True,min(y1,y2),max(y1,y2),True)

class VerticalTree(AVLTree):
    def insert(self,I,ls):
        if I.v1 is None or I.v2 is None: return
        super().insert(VerticalTreeValue(I,ls))
    def _findSplittingNode(self,HIq,VIq):
        n=self.root
        while n.L is not None or n.R is not None:
            Iy=n.S.recalculateY(HIq)
            if VIq.intersection(Iy) is not None:
                return n
            if Iy.v1<VIq.v1 and Iy.v2<VIq.v1:
                if n.L is None: return n
                n=n.L
            else:
                if n.R is None: return n
                n=n.R
        return n
    def _reportSubtree(self,rv,n):
        rv.append(n.S.value[2])
        if n.L is not None: rv=rv+self._reportSubtree(rv,n.L)
        if n.R is not None: rv=rv+self._reportSubtree(rv,n.R)
        return rv
    def query(self,HIq,VIq):
        rv=[]
        nsplit=self._findSplittingNode(HIq,VIq)
        if nsplit is None: return rv
        Iy=nsplit.S.recalculateY(HIq)
        if VIq.intersection(Iy) is not None: rv.append(nsplit.S.value[2])
        n=nsplit.L
        while n is not None:
            Iy=n.S.recalculateY(HIq)
            if VIq.intersection(Iy) is not None:
                rv.append(n.S.value[2])
                if n.R is not None: rv=rv+self._reportSubtree(rv,n.R)
                n=n.L
            else: n=n.R
        n=nsplit.R
        while n is not None:
            Iy=n.S.recalculateY(HIq)
            if VIq.intersection(Iy) is not None:
                rv.append(n.S.value[2])
                if n.L is not None: rv=rv+self._reportSubtree(rv,n.L)
                n=n.R
            else: n=n.L
        return rv

class STNode:
    I,S,T,leftChild,rightChild=None,[],None,None,None
    def __init__(self,v):
        self.S=[]
        self.value=v

class STValue(STNode):
    def __init__(self, v):
        super().__init__(v)

class SegmentTree:
    rootNode=None
    def __init__(self,ls):
        pts=set()
        for _ls in ls: pts=pts.union([_ls.p1.x,_ls.p2.x])
        pts=sorted(pts)
        ei,pt1=[],None
        for pt2 in pts:
            ei=ei+[Interval(False,pt1,pt2,False),Interval(True,pt2,pt2,True)]
            pt1=pt2
        ei=ei+[Interval(False,pt1,None,False)]
        self.rootNode=self._create(ei)
        self._insertSegments(ls)
    def _medium(self,ei):
        bds=[]
        lei=len(ei)
        if lei>0:
            if ei[0].v1 is None: bds.append(ei[0].v2)
            else: bds.append(ei[0].v1)
            if ei[lei-1].v2 is None: bds.append(ei[lei - 1].v1)
            else: bds.append(ei[lei-1].v2)
        return bds
    def _insertSegments(self,ls):
        for _ls in ls: self._insertSegment(self.rootNode,_ls)
    def _insertSegment(self,n,ls):
        if n.I.containedIn(ls):
            n.S.append(ls)
            if n.T is None: n.T=VerticalTree()
            n.T.insert(n.I,ls)
        else:
            if n.leftChild is not None:
                nl=n.leftChild
                if nl.I.intersection(ls) is not None: self._insertSegment(nl,ls)
            if n.rightChild is not None:
                nr=n.rightChild
                if nr.I.intersection(ls) is not None: self._insertSegment(nr,ls)
    def _create(self,ei):
        lei=len(ei)
        if lei==0: return None
        elif lei==1:
            n=STValue(mean(self._medium(ei)))
            n.I=Interval(ei[0].v1i, ei[0].v1, ei[lei - 1].v2, ei[lei - 1].v2i)
            return n
        else:
            vm=mean(self._medium(ei))
            m=ceil(lei/2)
            eileft=ei[0:m]
            eiright=ei[m:lei]
            nl,nr=self._create(eileft),self._create(eiright)
            n=STNode(vm)
            n.I=Interval(ei[0].v1i, ei[0].v1, ei[lei - 1].v2, ei[lei - 1].v2i)
            n.leftChild,n.rightChild=nl,nr
            return n
    def _SQFindSplittingNode(self,Iq):
        n=self.rootNode
        while n.leftChild is not None or n.rightChild is not None:
            lc,rc=n.leftChild,n.rightChild
            lci,rci=lc.I.containsEndpointsOf(Iq),rc.I.containsEndpointsOf(Iq)
            if lci==1 and rci==1:
                return n
            if lci==2: n=lc
            else: n=rc
        return n
    def _SQReportSubtree(self,n,VIq):
        rv=[]
        if n.T is not None: rv=rv+n.T.query(n.I,VIq)
        if n.leftChild is not None: rv=rv+self._SQReportSubtree(n.leftChild,VIq)
        if n.rightChild is not None: rv=rv+self._SQReportSubtree(n.rightChild,VIq)
        return rv
    def query(self,Wq):
        rv=set()
        (qx1,qx2),(qy1,qy2)=Wq[0],Wq[1]
        HIq,VIq=Interval(True,qx1,qx2,True),Interval(True,qy1,qy2,True)
        nsplit=self._SQFindSplittingNode(Wq[0])
        if nsplit is None: return rv
        if isinstance(nsplit,STValue):
            if len(nsplit.S)>0 and nsplit.T is not None:
                rv=rv.union(nsplit.T.query(HIq,VIq))
        else:
            n=nsplit.leftChild
            while n is not None and not isinstance(n,STValue):
                if n.T is not None:
                    rv=rv.union(n.T.query(Interval(True,qx1,n.I.v2,True),VIq))
                lc,rc=n.leftChild,n.rightChild
                if lc.I.inside(qx1):
                    rv=rv.union(self._SQReportSubtree(rc,VIq))
                    n=lc
                else: n=rc
            if n.T is not None:
                rv=rv.union(n.T.query(Interval(True,qx1,n.I.v2,True),VIq))
            n=nsplit.rightChild
            while n is not None and not isinstance(n,STValue):
                if n.T is not None:
                    rv=rv.union(n.T.query(Interval(True,n.I.v1,qx2,True),VIq))
                lc,rc=n.leftChild,n.rightChild
                if rc.I.inside(qx2):
                    rv=rv.union(self._SQReportSubtree(lc,VIq))
                    n=rc
                else: n=lc
            if n.T is not None:
                rv=rv.union(n.T.query(Interval(True,n.I.v1,qx2,True),VIq))
        return rv
