from math import ceil

class BTValue:
    pass
class BTNode:
    pass

class BTValue:
    value=None
    prev,next,lc,rc=None,None,None,None
    def __init__(self,value)->None:
        self.value=value
    def setnext(self,btv:BTValue)->None:
        self.next=btv
        if btv is not None:
            btv.prev=self
    def setleftchild(self,lc:BTNode,pn:BTValue=None)->None:
        self.lc=lc
        if self.lc is not None:
            if pn is not None:
                self.lc.pn=pn
            self.lc.pv=self
    def setrightchild(self,rc:BTNode,pn:BTValue=None)->None:
        self.rc=rc
        if self.rc is not None:
            if pn is not None:
                self.rc.pn=pn
            self.rc.pv=self
    def clearleftchild(self)->None:
        self.lc=None
    def clearrightchild(self)->None:
        self.rc=None

class BTNode:
    start,last,pn,pv,orphan=None,None,None,None,None
    size,deg=0,5
    def __init__(self,value=None,start:BTValue=None,deg:int=5,initsize:int=1)->None:
        if value is not None: self.start=BTValue(value)
        if start is not None: self.start=start
        self.last=self.start
        self.size=initsize
        self.deg=deg
    def search(self,value)->(BTNode,BTValue):
        if self.start is None: return (self,None)
        v=self.start
        while v.value<value and v.next is not None:
            v=v.next
        if v.value==value: return (self,v)
        elif v.next is None and v.value<value:
            if v.rc is not None:
                return v.rc.search(value)
            else: return (self,None)
        else:
            if v.lc is not None:
                return v.lc.search(value)
            else: return (self,None)
    def insert(self,value)->BTValue:
        v=self.start
        while v is not None and v.value<=value:
            v=v.next
        nv=BTValue(value)
        if v is not None:
            pv=v.prev
            nv.setnext(v)
            if pv is not None:
                pv.setnext(nv)
            else:
                self.start=nv
        else:
            if self.last is not None:
                self.last.setnext(nv)
            else:
                self.start=nv
        if nv.next is None:
            self.last=nv
        self.size=self.size+1
        return nv
    def _adjustParent(self)->None:
        v=self.start
        while v is not None:
            if v.lc is not None: v.lc.pn=self
            if v.rc is not None: v.rc.pn=self
            v=v.next
    def split(self)->BTNode:
        if self.size>=self.deg:
            s=ceil(self.deg/2)-1
            nl=BTNode(start=self.start,deg=self.deg,initsize=s)
            nl.pn=self.pn
            v=self.start
            for i in range(s-1): v=v.next
            nm=v.next
            v.next=None
            v.setrightchild(nm.lc)
            nl.last=v
            nl._adjustParent()
            nr=self
            nr.start,nr.size=nm.next,nr.size-1-s
            nm.next,nr.start.prev=None,None
            if nr.pn is not None: # 2b
                nv=nr.pn.insert(nm.value)
                nv.setleftchild(nl)
                if nv.next is None:
                    nv.setrightchild(nv.prev.rc)
                    nv.prev.setrightchild(None)
                if nr.pn is not None: return nr.pn.split()
            else: # 2a
                nroot=BTNode(value=nm.value,deg=self.deg,initsize=1)
                nl.pn,nr.pn=nroot,nroot
                nroot.start.setleftchild(nl)
                nroot.start.setrightchild(nr)
                return nroot
        return None
    def _maxvalue(self)->(BTNode,BTValue):
        if self.last is None: return (self,None)
        if self.last.rc is not None:
            return self.last.rc.maxvalue()
        else:
            return (self,self.last)
    def _minvalue(self)->(BTNode,BTValue):
        if self.start is None: return (self,None)
        if self.start.lc is not None:
            return self.start.lc.minvalue()
        else:
            return (self,self.start)
    def _siblings(self)->(BTNode,BTNode):
        ps,ss,pv=None,None,self.pv
        if pv is not None:
            if pv.lc==self:
                if pv.prev is not None:
                    ps=pv.prev.lc
                if pv.rc is not None:
                    ss=pv.rc
                elif pv.next is not None:
                    ss=pv.next.lc
            elif pv.rc==self:
                ps=pv.lc
        return (ps,ss)
    def _removevalue(self,v:BTValue)->(BTValue,BTValue,BTValue):
        pv,nv=v.prev,v.next
        if pv is None:
            if nv is not None:
                self.start=nv
                nv.prev=None
            else:
                self.start,self.last=None,None
        else:
            if nv is not None:
                pv.next=nv
                nv.prev=pv
            else:
                pv.next=None
                self.last=pv
        self.size=self.size-1
        return (pv,v,nv)
    def _shiftleft(self,nl:BTNode,v:BTValue,nr:BTNode)->None:
        if v.value is None: return
        nl.insert(v.value)
        if nl.last.prev is not None:
            nl.last.setleftchild(nl.last.prev.rc,nl)
            nl.last.prev.clearrightchild()
        elif nl.orphan is not None:
            nl.last.setleftchild(nl.orphan,nl)
            nl.orphan=None
        if nr.size>0:
            nl.last.setrightchild(nr.start.lc,nl)
            if nr.size==1:
                nr.orphan=nr.start.rc
            v.value=nr.start.value
            nr._removevalue(nr.start)
        else:
            nl.last.setrightchild(nr.orphan,nl)
            v.value=None
            nr.orphan=None
    def _shiftright(self,nl:BTNode,v:BTValue,nr:BTNode)->None:
        nr.insert(v.value)
        if nr.orphan is not None:
            nr.start.setrightchild(nr.orphan,nr)
            nr.orphan=None
        if nl.last is not None:
            nr.start.setleftchild(nl.last.rc,nr)
            v.value=nl.last.value
            if nl.last.prev is not None:
                nl.last.prev.setrightchild(nl.last.lc)
            nl._removevalue(nl.last)
        else:
            nr.start.setleftchild(nl.orphan,nr)
            nl.orphan=None
            v.value=None
    def _redistribute(self,nl:BTNode,v:BTValue,nr:BTNode)->None:
        while self.size<ceil(self.deg/2)-1:
            if nl is self: self._shiftleft(nl, v, nr)
            else: self._shiftright(nl, v, nr)
    def _merge(self,nl:BTNode,v:BTValue,nr:BTNode)->None:
        while self.size>0 or v.value is not None:
            if nl is self: self._shiftright(nl, v, nr)
            else: self._shiftleft(nl, v, nr)
        nn=nl
        if nl is self: nn=nr
        if self.pn.size==1:
            if self.pn.pn is None:
                nn.pn,nn.pv=None,None
                return nn
            else:
                self.pn.orphan=nn
                self.pn._removevalue(v)
        elif v.next is None:
            v.prev.setrightchild(nn,self.pn)
            self.pn._removevalue(v)
        else:
            v.next.setleftchild(nn,self.pn)
            self.pn._removevalue(v)
        return None
    def removal_consolidate(self)->BTNode:
        nroot=None
        if self.size<ceil(self.deg/2)-1:
            (ps,ss)=self._siblings()
            pn=self.pn
            if ps is not None:
                if ps.size>ceil(self.deg/2)-1:
                    self._redistribute(ps, ps.pv, self)
                else:
                    nroot=self._merge(ps,ps.pv,self)
            elif ss is not None:
                if ss.size>ceil(self.deg/2)-1:
                    self._redistribute(self, self.pv, ss)
                else:
                    nroot=self._merge(self,self.pv,ss)
            if nroot is None and pn is not None:
                nroot=pn.removal_consolidate()
        return nroot
    def remove(self,v:BTValue)->BTNode:
        if v.lc is not None:
            (n,pv)=v.lc._maxvalue()
            v.value=pv.value
            n._removevalue(pv)
            return n
        else:
            self._removevalue(v)
            return self
    
class BTree:
    root:BTNode
    deg:int
    root,deg=None,5
    def __init__(self,value,deg=5):
        self.root=BTNode(value,deg=deg)
        self.deg=deg
    def search(self,value)->BTValue:
        (n,v)=self.root.search(value)
        return v
    def _insert(self,val)->None:
        (n,v)=self.root.search(val)
        n.insert(val)
        nroot=n.split()
        if nroot is not None: self.root=nroot
    def insert(self,value)->None:
        if type(value) is list:
            for v in value:
                self._insert(v)
        else: self._insert(value)
    def _remove(self,val)->None:
        (n,v)=self.root.search(val)
        if v is not None:
            n=n.remove(v)
            nroot=n.removal_consolidate()
            if nroot is not None: self.root=nroot
    def remove(self,value)->None:
        if type(value) is list:
            for v in value:
                self._remove(v)
        else: self._remove(value)
