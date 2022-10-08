class Node:
    S=None
    L,R,P=None,None,None
    h=1
    def __init__(self,v):
        self.S=v
    def setLeftChild(self,n):
        self.L=n
        if n is not None: n.P=self
    def setRightChild(self,n):
        self.R=n
        if n is not None: n.P=self
    def toRoot(self):
        self.P=None
        return self
    def query(self,v):
        if v<self.S and self.L is not None:
            return self.L.query(v)
        elif v>self.S and self.R is not None:
            return self.R.query(v)
        else:
            return self
    def insert(self,v):
        n=self.query(v)
        if v<n.S: n.setLeftChild(Node(v))
        elif v>n.S: n.setRightChild(Node(v))
        else: raise Exception('cannot insert')
        return n
    def children(self):
        c=0
        if self.L is not None: c=c+1
        if self.R is not None: c=c+1
        return c
    def rightmost(self):
        if self.R is not None: return self.R.rightmost()
        else: return self
    def leftmost(self):
        if self.L is not None: return self.L.leftmost()
        else: return self
    def rightrotate(self,tree):
        C=self.L
        if C is None: return
        A=self.P
        if A is not None:
            if A.L is self: A.setLeftChild(C)
            if A.R is self: A.setRightChild(C)
        else: tree.root=C.toRoot()
        t=C.R
        C.setRightChild(self)
        self.setLeftChild(t)
    def leftrotate(self,tree):
        C=self.R
        if C is None: return
        A=self.P
        if A is not None:
            if A.L is self: A.setLeftChild(C)
            if A.R is self: A.setRightChild(C)
        else: tree.root=C.toRoot()
        t=C.L
        C.setLeftChild(self)
        self.setRightChild(t)
    def nodes(self):
        res=1
        if self.L is not None:
            res=res+self.L.nodes()
        if self.R is not None:
            res=res+self.R.nodes()
        return res
    def depth(self):
        resL,resR=0,0
        if self.L is not None:
            resL=self.L.depth()
        if self.R is not None:
            resR=self.R.depth()
        return 1+max(resL,resR)
    def updateHeight(self):
        l,r=0,0
        if self.L is not None:
            l=self.L.h
        if self.R is not None:
            r=self.R.h
        self.h=1+max(l,r)
    def bal_factor(self):
        l,r=0,0
        if self.L is not None:
            l=self.L.h
        if self.R is not None:
            r=self.R.h
        return r-l

class SimpleBinaryTree:
    root=None
    def __init__(self,root=None):
        self.root=root
    def nodes(self):
        if self.root is None:
            return 0
        else:
            return self.root.nodes()
    def isBalanced(self):
        if self.root is None:
            return True
        else:
            dL,dR=0,0
            if self.root.L is not None:
                dL=self.root.L.depth()
            if self.root.R is not None:
                dR=self.root.R.depth()
            return abs(dL-dR)<2
    def query(self,v):
        if self.root is None: return None
        else:
            n=self.root.query(v)
            if v==n.S: return n
            else: return None
    def insert(self,v):
        if self.root is None:
            self.root=Node(v)
            return None
        else:
            return self.root.insert(v)
    def remove(self,v):
        if self.root is None: return
        n=self.root.query(v)
        fp=n.P
        c=n.children()
        if c==0 and n.P is None: self.root=None
        elif c==0 and n.P is not None:
            if n.P.L is n: n.P.setLeftChild(None)
            elif n.P.R is n: n.P.setRightChild(None)
        elif c==1 and n.P is None:
            if n.L is not None: self.root=n.L.toRoot()
            elif n.R is not None: self.root=n.R.toRoot()
        elif c==1 and n.P is not None:
            if n.P.L is n:
                if n.L is not None: n.P.setLeftChild(n.L)
                elif n.R is not None: n.P.setLeftChild(n.R)
            elif n.P.R is n:
                if n.L is not None: n.P.setRightChild(n.L)
                elif n.R is not None: n.P.setRightChild(n.R)
        elif c==2: # by copy
            pred=n.L.rightmost()
            val=pred.S
            fp=self.remove(pred.S)
            n.S=val
        return fp
    def rightbackbone(self):
        B=self.root
        while B is not None:
            C=B.L
            if C is not None:
                B.rightrotate(self)
                B=C
            else:
                B=B.R
