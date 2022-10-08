from statistics import median

def FindSplittingNode(tau,mu1,mu2):
    n=tau.rootNode
    while not isinstance(n,Value) and ((mu1 is not None and mu1>=n.value) or (mu2 is not None and mu2<=n.value)):
        if mu2<=n.value:
            if n.leftChild is not None: n=n.leftChild
            else: return None
        else:
            if n.rightChild is not None: n=n.rightChild
            else: return None
    return n

def ReportSubtree(rv,n):
    if n is not None:
        if isinstance(n,Value): rv.append(n)
        else:
            ReportSubtree(rv,n.leftChild)
            ReportSubtree(rv,n.rightChild)

def OneDRangeQuery(tau,axis,mu1,mu2):
    rv=[]
    nsplit=FindSplittingNode(tau,mu1,mu2)
    if nsplit is None: return rv
    if isinstance(nsplit,Value):
        if nsplit.isInRangeAxis(axis,mu1,mu2): rv.append(nsplit.value)
    else:
        n=nsplit.leftChild
        while n is not None and not isinstance(n,Value):
            if mu1 is not None and mu1<=n.value['point'][axis]:
                ReportSubtree(rv,n.rightChild)
                n=n.leftChild
            else: n=n.rightChild
        if n is not None and isinstance(n,Value) and n.isInRangeAxis(axis,mu1,mu2):
            rv.append(n.value)
        n=nsplit.rightChild
        while n is not None and not isinstance(n,Value):
            if mu2 is not None and n.value['point'][axis]<=mu2:
                ReportSubtree(rv,n.leftChild)
                n=n.rightChild
            else: n=n.leftChild
        if n is not None and isinstance(n,Value) and n.isInRangeAxis(axis,mu1,mu2):
            rv.append(n.value)
    return rv

class Node:
    value,leftChild,rightChild,nlevel=None,None,None,None
    def __init__(self,v):
        self.value=v

class Value(Node):
    def __init__(self, v):
        self.value=[]
        if type(v) is list:
            for v1 in v:
                self.value.append(v1)
        else: self.value.append(v)
    def isInRange(self,qx1=None,qx2=None,qy1=None,qy2=None):
        if not self.isInRangeAxis(0,qx1,qx2): return False
        if not self.isInRangeAxis(1,qy1,qy2): return False
        return True
    def isInRangeAxis(self,axis,mu1,mu2):
        for v in self.value:
            if mu1 is not None and v['point'][axis]<mu1: return False
            if mu2 is not None and v['point'][axis]>mu2: return False
        return True

class BinaryTreeWithLeafValues:
    rootNode=None
    def __init__(self,Pp,axis=0):
        self.rootNode=self._create(Pp,axis)
    def _create(self,Pp,axis):
        if len(Pp)==0: return None
        tau_asoc=None
        if axis+1<2:
            tau_asoc=BinaryTreeWithLeafValues(Pp,axis+1)
        dist_vals=set(map(lambda p:p['point'][axis],Pp))
        if len(Pp)==1 or len(dist_vals)==1:
            n=Value(Pp)
            if tau_asoc is not None: n.nlevel=tau_asoc
        else:
            a_vals=list(map(lambda p:p['point'][axis],Pp))
            vm=median(a_vals)
            Ppleft=list(filter(lambda p:p['point'][axis]<=vm,Pp))
            Ppright=list(filter(lambda p:p['point'][axis]>vm,Pp))
            nl,nr=self._create(Ppleft,axis),self._create(Ppright,axis)
            n=Node(vm)
            n.leftChild,n.rightChild=nl,nr
            if tau_asoc is not None:
                n.nlevel=tau_asoc
        return n
    def TwoDRangeQuery(self,x1,x2,y1,y2):
        rv=[]
        nsplit=FindSplittingNode(self,x1,x2)
        if nsplit is None: return rv
        if isinstance(nsplit,Value):
            if nsplit.isInRange(x1,x2,y1,y2): rv.append(nsplit.value)
        else:
            n=nsplit.leftChild
            while n is not None and not isinstance(n,Value):
                if x1 is None or (x1 is not None and x1<=n.value):
                    rv=rv+OneDRangeQuery(n.rightChild.nlevel,1,y1,y2)
                    n=n.leftChild
                else: n=n.rightChild
            if n is not None and isinstance(n,Value) and n.isInRange(x1,x2,y1,y2):
                rv.append(n.value)
            n=nsplit.rightChild
            while n is not None and not isinstance(n,Value):
                if x2 is None or (x2 is not None and n.value<=x2):
                    rv=rv+OneDRangeQuery(n.leftChild.nlevel,1,y1,y2)
                    n=n.rightChild
                else: n=n.leftChild
            if n is not None and isinstance(n,Value) and n.isInRange(x1,x2,y1,y2):
                rv.append(n.value)
        return rv

