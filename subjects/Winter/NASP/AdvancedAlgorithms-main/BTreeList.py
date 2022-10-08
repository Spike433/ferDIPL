from math import floor,ceil

class BTNode:
    pass

class BTNode:
    L:list
    P:BTNode
    deg:int
    L,P,deg=[],None,5
    def __init__(self,value:int=None,L:list=None,deg:int=5,P:BTNode=None)->None:
        if value is not None: self.L=[None,value,None]
        else:
            self.L=L
            for item in self.L:
                if type(item) is BTNode: item.P=self
        self.deg=deg
        self.P=P
    def searchValue(self,value:int)->(BTNode,bool,int):
        for index in range(len(self.L)):
            item=self.L[index]
            if type(item) is int:
                lc=self.L[index-1]
                if value==item: return (self,True,index)
                if value<item:
                    if lc is not None: return lc.searchValue(value)
                    else: return (self,False,index)
        rc=self.L[len(self.L)-1]
        if rc is not None: return rc.searchValue(value)
        else: return (self,False,len(self.L))
    def keys(self)->int:
        return int((len(self.L)-1)/2)
    def minKeys(self)->int:
        return ceil(self.deg/2)-1
    def insertValue(self,value:int):
        (n,f,i)=self.searchValue(value)
        if not f:
            if i<len(n.L): n.L[i:i]=[value,None]
            else: n.L+=[value,None]
            return n._split()
        return None
    def _split(self)->BTNode:
        if self.keys()>(self.deg-1):
            i=self.minKeys()*2+1
            nl,nv,nr=BTNode(L=self.L[:i],deg=self.deg,P=self.P),self.L[i],BTNode(L=self.L[i+1:],deg=self.deg,P=self.P)
            if self.P is None:
                nroot=BTNode(L=[nl,nv,nr],deg=self.deg)
                nl.P,nr.P=nroot,nroot
                return nroot
            else:
                for index in range(len(self.P.L)):
                    if self.P.L[index] is self:
                        self.P.L=self.P.L[:index]+[nl,nv,nr]+self.P.L[index+1:]
                        return self.P._split()
        return None
    def _rightMost(self)->(BTNode,int):
        if self.L[-1] is not None: return self.L[-1]._rightMost()
        else: return (self,self.L[-2])
    def _removeValue(self,index:int)->BTNode:
        if self.L[index-1] is not None:
            (n,v)=self.L[index-1]._rightMost()
            self.L[index]=v
            return n._removeValue(len(n.L)-2)
        else:
            self.L=self.L[:index]+self.L[index+2:]
            return self
    def _siblings(self)->(BTNode,int,BTNode,int):
        if self.P is not None:
            p,pi,s,si=None,None,None,None
            for index in range(len(self.P.L)):
                if self.P.L[index] is self:
                    ipr,isu=index-2,index+2
                    if 0<=ipr<len(self.P.L): p,pi=self.P.L[ipr],index-1
                    if 0<=isu<len(self.P.L): s,si=self.P.L[isu],index+1
                    break
            return (p,pi,s,si)
        return (None,None,None,None)
    def _redistribute(self,s:BTNode,ci:int,pred:bool=True)->BTNode:
        if pred: cmn=BTNode(L=s.L+[self.P.L[ci]]+self.L,deg=self.deg)
        else: cmn=BTNode(L=self.L+[self.P.L[ci]]+s.L,deg=self.deg)
        center=self.minKeys()*2+1
        self.P.L[ci]=cmn.L[center]
        nl,nr=BTNode(L=cmn.L[:center],deg=self.deg,P=self.P),BTNode(L=cmn.L[center+1:],deg=self.deg,P=self.P)
        self.P.L[ci-1],self.P.L[ci+1]=nl,nr
        return self.P
    def _merge(self,s:BTNode,ci:int,pred:bool=True)->BTNode:
        if pred: cmn=BTNode(L=s.L+[self.P.L[ci]]+self.L,deg=self.deg,P=self.P)
        else: cmn=BTNode(L=self.L+[self.P.L[ci]]+s.L,deg=self.deg,P=self.P)
        self.P.L[ci-1]=cmn
        self.P.L=self.P.L[:ci]+self.P.L[ci+2:]
        return self.P
    def _consolidate(self)->BTNode:
        if self.P is None and len(self.L)==1:
            self.L[0].P=None
            return self.L[0]
        k,mk=self.keys(),self.minKeys()
        if self.keys()<self.minKeys():
            (p,pi,s,si)=self._siblings()
            if p is not None: sib,sib_i,sib_p=p,pi,True
            else: sib,sib_i,sib_p=s,si,False
            if sib is not None:
                tot=sib.keys()+1+self.keys()
                if tot>self.deg-1: n=self._redistribute(sib,sib_i,sib_p)
                else: n=self._merge(sib,sib_i,sib_p)
                if n is not None: return n._consolidate()
        return None
    def removeValue(self,value:int)->BTNode:
        (n,f,i)=self.searchValue(value)
        if f:
            n=n._removeValue(i)
            return n._consolidate()
        return None
    def __str__(self)->str:
        res="|"
        for item in self.L:
            if type(item) is int:
                res+="{}".format(item)
            if type(item) is BTNode:
                res+="[K]"
            if item is None:
                res+="[N]"
        res+="|"
        return res

class BTreeList:
    root:BTNode
    deg:int
    root,deg=None,5
    def __init__(self,value:int,deg:int=5)->None:
        self.root=BTNode(value=value,deg=deg)
    def searchValue(self,value:int)->bool:
        (n,f,i)=self.root.searchValue(value)
        return f
    def insertValue(self,value:int)->None:
        nroot=self.root.insertValue(value)
        if nroot is not None: self.root=nroot
    def removeValue(self,value:int)->None:
        nroot=self.root.removeValue(value)
        if nroot is not None: self.root=nroot
    def insertValues(self,values:list[int])->None:
        for v in values:
            nroot=self.root.insertValue(v)
            if nroot is not None: self.root=nroot
    def removeValues(self,values:list[int])->None:
        for v in values:
            nroot=self.root.removeValue(v)
            if nroot is not None: self.root=nroot
    def __str__(self)->str:
        res=""
        q=[self.root,"\n"]
        while q!=["\n"]:
            n=q[0]
            q=q[1:]
            if type(n) is str:
                res+=n
                q.append("\n")
            else:
                res+=str(n)
                for item in n.L:
                    if type(item) is BTNode: q.append(item)
        return res

def testNode(n1:BTNode,n2:BTNode)->(bool,str):
    if len(n1.L)!=len(n2.L): return (False,"Duljina čvora nije ispravna... fale pokazivači, vrijednosti!? Ispravni čvor:{}, Vaš čvor:{}".format(n1,n2))
    for index in range(len(n1.L)):
        if type(n1.L[index]) is int:
            v1,v2=n1.L[index],n2.L[index]
            if v1!=v2: return (False,"Vrijednost {} nije na ispravnom mjestu! Ispravni čvor:{}, Vaš čvor:{}".format(v2,n1,n2))
            if n1.L[index-1] is None and n2.L[index-1] is not n1.L[index-1]:
                return (False,"Greška u pokazivaču lijevog djeteta za vrijednost {}. Pokazivač treba biti None! Ispravni čvor:{}, Vaš čvor:{}".format(v2,n1,n2))
            if n1.L[index-1] is not None and type(n2.L[index-1]) is not BTNode:
                return (False,"Greška u pokazivaču lijevog djeteta za vrijednost {}. Treba postojati pokazivač, ovo je unutarnji čvor! Ispravni čvor:{}, Vaš čvor:{}".format(v2,n1,n2))
            if n1.L[index-1] is not None:
                (res,res_s)=testNode(n1.L[index-1],n2.L[index-1])
                if not res: return (res,res_s)
    if n1.L[-1] is None and n2.L[-1] is not n1.L[-1]:
        return (False,"Greška u pokazivaču lijevog djeteta za vrijednost {}. Pokazivač treba biti None! Ispravni čvor:{}, Vaš čvor:{}".format(v2,n1,n2))
    if n1.L[-1] is not None and type(n2.L[-1]) is not BTNode:
        return (False,"Greška u pokazivaču lijevog djeteta za vrijednost {}. Treba postojati pokazivač, ovo je unutarnji čvor! Ispravni čvor:{}, Vaš čvor:{}".format(v2,n1,n2))
    if n1.L[-1] is not None:
        (res,res_s)=testNode(n1.L[-1],n2.L[-1])
        if not res: return (res,res_s)
    return (True,None)

