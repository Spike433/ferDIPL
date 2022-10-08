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

