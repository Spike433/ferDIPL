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



