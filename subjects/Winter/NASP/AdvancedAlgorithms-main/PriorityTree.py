from statistics import median
from GeomGeneral import isInRange

class Node:
    p,leftChild,rightChild,y=None,None,None,None
    def __init__(self,p):
        self.p=p
        self.y=p[1]
    def __str__(self):
        return '({},{})'.format(self.p[0],self.p[1])

class PriorityTree:
    rootNode=None
    def __init__(self,Pp):
        Pp=list(sorted(Pp,key=lambda p:p[0]))
        self.rootNode=self._create(Pp)
    def _create(self,Pp):
        pmin=Pp[0]
        n=Node(pmin)
        del Pp[0]
        if len(Pp)>0:
            ymed=median(map(lambda it:it[1],Pp))
            n.y=ymed
            Pl=list(filter(lambda it:it[1]<=ymed,Pp))
            if len(Pl)>0: n.leftChild=self._create(Pl)
            Pr=list(filter(lambda it:it[1]>ymed,Pp))
            if len(Pr)>0: n.rightChild=self._create(Pr)
        return n
    def _findSplittingNode(self,qy1,qy2):
        n,rn=self.rootNode,[]
        while n is not None and (qy1>n.y or qy2<n.y):
            rn.append(n)
            if qy2<n.y:
                if n.leftChild is not None: n=n.leftChild
                else: return None,rn
            else:
                if n.rightChild is not None: n=n.rightChild
                else: return None,rn
        return n,rn
    def _queryPrioritySubtree(self,n,qx2):
        res=[]
        if n is not None and n.p[0]<=qx2:
            res.append(n.p)
            res=res+self._queryPrioritySubtree(n.leftChild,qx2)
            res=res+self._queryPrioritySubtree(n.rightChild,qx2)
        return res
    def Query(self,qx2,qy1,qy2):
        rv=[]
        nsplit,rn=self._findSplittingNode(qy1,qy2)
        for n in rn:
            if n.p[0]<=qx2 and isInRange(qy1,n.p[1],qy2): rv.append(n.p)
        if nsplit is None: return rv
        if nsplit.leftChild is None and nsplit.rightChild is None:
            rv=rv+self._queryPrioritySubtree(nsplit,qx2)
        else:
            if nsplit.p[0]<=qx2 and isInRange(qy1,nsplit.p[1],qy2): rv.append(nsplit.p)
            n=nsplit.leftChild
            while n is not None and n.p[0]<=qx2:
               if isInRange(qy1,n.p[1],qy2): rv.append(n.p)
               if isInRange(qy1,n.y,qy2):
                   rv=rv+self._queryPrioritySubtree(n.rightChild,qx2)
                   n=n.leftChild
               else: n=n.rightChild
            n=nsplit.rightChild
            while n is not None and n.p[0]<=qx2:
               if isInRange(qy1,n.p[1],qy2): rv.append(n.p)
               if isInRange(qy1,n.y,qy2):
                   rv=rv+self._queryPrioritySubtree(n.leftChild,qx2)
                   n=n.rightChild
               else: n=n.leftChild
        return rv


