from statistics import median
from GeomGeneral import  isInRange

class Node:
    value,leftChild,rightChild=None,None,None
    def __init__(self,v):
        self.value=v
    def insert(self,v):
        if v<self.value:
            if self.leftChild is not None:
                if not isinstance(self.leftChild,Value):
                    self.leftChild.insert(v)
                else:
                    t=self.leftChild
                    self.leftChild=Node(v)
                    if t.value<v:
                        self.leftChild.leftChild=t
                        self.leftChild.rightChild=Value(v)
                    else:
                        self.leftChild.leftChild=Value(v)
                        self.leftChild.rightChild=t
            else:
                self.leftChild=Node(v)
                self.leftChild.leftChild=Value(v)
        elif v>self.value:
            if self.rightChild is not None:
                if not isinstance(self.rightChild,Value):
                    self.rightChild.insert(v)
                else:
                    t=self.rightChild
                    self.rightChild=Node(v)
                    if t.value<v:
                        self.rightChild.leftChild=t
                        self.rightChild.rightChild=Value(v)
                    else:
                        self.rightChild.leftChild=Value(v)
                        self.rightChild.rightChild=t
            else:
                self.rightChild=Node(v)
                self.rightChild.leftChild=Value(v)

class Value(Node):
    def __init__(self, v):
        super().__init__(v)

class BinaryTreeWithLeafValues:
    rootNode=None
    def __init__(self,rootValue=None,Pp=None):
        if rootValue is not None:
            self.rootNode=Node(rootValue)
            self.rootNode.leftChild=Value(rootValue)
        elif Pp is not None:
            self.rootNode=self._create(Pp)
    def insert(self,value):
        if self.rootNode is not None:
            if isinstance(value,list):
                for item in value:
                    self.rootNode.insert(item)
            else: self.rootNode.insert(value)
    def _create(self,Pp):
        if len(Pp)==1: return Value(Pp[0])
        else:
            vm=median(Pp)
            Ppleft=list(filter(lambda p:p<=vm,Pp))
            Ppright=list(filter(lambda p:p>vm,Pp))
            nl,nr=self._create(Ppleft),self._create(Ppright)
            n=Node(vm)
            n.leftChild,n.rightChild=nl,nr
            return n

def FindSplittingNode(tau,mu1,mu2):
    n=tau.rootNode
    while not isinstance(n,Value) and ((mu1 is not None and mu1>=n.value) or (mu2 is not None and mu2<=n.value)):
        if mu2 is not None and mu2<=n.value:
            if n.leftChild is not None: n=n.leftChild
            else: return None
        elif mu1 is not None and mu1>=n.value:
            if n.rightChild is not None: n=n.rightChild
            else: return None
        else: raise Exception('cannot find the splitting node due to inconsistent conditions')
    return n

def ReportSubtree(rv,n):
    if n is not None:
        if isinstance(n,Value): rv.append(n)
        else:
            ReportSubtree(rv,n.leftChild)
            ReportSubtree(rv,n.rightChild)

def OneDRangeQuery(tau,mu1,mu2):
    rv=[]
    nsplit=FindSplittingNode(tau,mu1,mu2)
    if nsplit is None: return rv
    if isinstance(nsplit,Value):
        if isInRange(mu1,nsplit.value,mu2): rv.append(nsplit)
    else:
        n=nsplit.leftChild
        while n is not None and not isinstance(n,Value):
            if mu1 is not None and mu1<=n.value:
                ReportSubtree(rv,n.rightChild)
                n=n.leftChild
            else: n=n.rightChild
        if n is not None and isinstance(n,Value) and isInRange(mu1,n.value,mu2):
            rv.append(n)
        n=nsplit.rightChild
        while n is not None and not isinstance(n,Value):
            if mu2 is not None and n.value<=mu2:
                ReportSubtree(rv,n.leftChild)
                n=n.rightChild
            else: n=n.leftChild
        if n is not None and isinstance(n,Value) and isInRange(mu1,n.value,mu2):
            rv.append(n)
    return rv


