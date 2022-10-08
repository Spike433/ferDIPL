class Node:
    v,p=None,None
    def __init__(self,v):
        self.v=v
    def search(self,v):
        if (self.v is None or v>self.v) and self.p is not None:
            return self.p.search(v)
        elif self.v is not None and self.v==v: return self
        else: return None
    def insert(self,v):
        nv=None
        if self.p is not None: nv=self.p.v
        if (self.v is None or v>self.v) and (nv is None or v<nv):
            tp=self.p
            self.p=Node(v)
            self.p.p=tp
        elif self.v is not None and v==self.v: return
        else: self.p.insert(v)

class List:
    head=Node(None)
    def search(self,v):
        return self.head.search(v)
    def insert(self,v):
        self.head.insert(v)


