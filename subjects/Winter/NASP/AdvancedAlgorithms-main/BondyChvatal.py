from copy import deepcopy
from random import choice
from math import floor,ceil

class BCGraph():
    def __init__(self,nodes:list) -> None:
        self.nodes=nodes
        self.G={n1:{n2:0 for n2 in nodes} for n1 in nodes}
        self.EG=deepcopy(self.G)
    def addEdges(self,edgs:list) -> None:
        for (n1,n2) in edgs:
            self.G[n1][n2]=self.G[n2][n1]=1
    def _genHc(self,HcE:list) -> dict:
        Hc=deepcopy(self.EG)
        for (n1,n2) in HcE:
            Hc[n1][n2]=Hc[n2][n1]=1
        return Hc
    def _genHcE(self,Hc:dict) -> list:
        _Hc=deepcopy(Hc)
        res=[]
        for n1 in _Hc:
            for n2 in _Hc[n1]:
                if _Hc[n1][n2]>0 and _Hc[n2][n1]>0:
                    res.append((n1,n2))
                    _Hc[n1][n2]=_Hc[n2][n1]=0
        return res
    def addEdge(self,n1:chr,n2:chr,m:dict,i:int) -> None:
        m[n1][n2]=m[n2][n1]=i
    def _ae(self,n:chr,m:dict) -> int:
        ta=0
        for n1 in self.nodes:
            if m[n][n1]>0: ta=ta+1
        return ta
    def _hasEdge(self,n1:chr,n2:chr,aem:dict,chkOrig:bool=True) -> bool:
        return (chkOrig and self.G[n1][n2]>0) or aem[n1][n2]>0
    def _checkPair(self,n1:chr,n2:chr,aem:dict) -> bool:
        return self._ae(n1,self.G)+self._ae(n2,self.G)+self._ae(n1,aem)+self._ae(n2,aem)>=len(self.nodes)
    def checkClosure(self,addedgs:dict) -> (bool,list):
        i=1
        aem=deepcopy(self.EG)
        res=True
        errs=[]
        while True:
            k=str(i)
            if k in addedgs.keys():
                edg=addedgs[str(i)]
                (n1,n2)=edg
                if self.G[n1][n2]>0:
                    res=False
                    errs.append("Dodani brid ({},{}) već postoji u početnom grafu G".format(n1,n2))
                elif aem[n1][n2]>0:
                    res=False
                    errs.append("Dodani brid ({},{}) već ste prije dodali u postupku stvaranja zatvarača".format(n1,n2))
                elif not self._checkPair(n1,n2,aem):
                    res=False
                    errs.append("Brid ({},{}) ne možete dodati u ovom trenutku jer zbroj stupnjeva priležećih vrhova nije >={}".format(n1,n2,len(self.nodes)))
                else:
                    self.addEdge(n1,n2,aem,i)
            else:
                break
            i=i+1
        for n1 in self.G:
            for n2 in self.G[n1]:
                if n1!=n2 and not self._hasEdge(n1,n2,aem) and self._checkPair(n1,n2,aem):
                    res=False
                    errs.append("Dodanim bridovima još niste stvorili zatvarač G'. Još uvijek možete dodavati bridove, npr. ({},{})!".format(n1,n2))
                    return (res,errs)
        if res:
            self.closure=aem
        return (res,errs)
    def checkHc(self,cHcE:list,tHcE:list) -> (bool,list):
        cHc=self._genHc(cHcE)
        tHc=self._genHc(tHcE)
        res=True
        errs=[]
        for n in tHc:
            if self._ae(n,tHc)!=2:
                res=False
                errs.append("Vrh {} u vašem Hamiltonovom ciklusu nema točno dva priležeća brida!".format(n))
        for (n1,n2) in tHcE:
            if cHc[n1][n2]==0 or cHc[n2][n1]==0:
                res=False
                errs.append("Brid ({},{}) u vašem Hamiltonovom ciklusu ne postoji u ispravnom i očekivanom Hamiltonovom ciklusu!".format(n1,n2))
            cHc[n1][n2]=cHc[n2][n1]=0
        for n1 in cHc:
            for n2 in cHc[n1]:
                if cHc[n1][n2]>0 or cHc[n2][n1]>0:
                    res=False
                    errs.append("U vašem Hamiltonovom ciklusu ne postoji brid koji postoji u ispravnom i očekivanom Hamiltonovom ciklusu, npr. ({},{})".format(n1,n2))
                    return (res,errs)
        return (res,errs)
    def bckStep(self,step:int,change:dict,HcE:list) -> (bool,list,list):
        (u,v)=change["uv"]
        (p,q)=change["pq"]
        Hc=self._genHc(HcE)
        res,errs=True,[]
        for n in Hc:
            if self._ae(n,Hc)!=2:
                res=False
                errs.append("Vrh {} u trenutnom Hamiltonovom ciklusu nema točno dva priležeća brida!".format(n))
        m,n=-1,{(u,v):-1,(p,q):-1}
        for n1 in Hc:
            for n2 in Hc[n1]:
                if Hc[n1][n2]>0 or Hc[n2][n1]>0:
                    if self.closure[n1][n2]>0 and m<self.closure[n1][n2]: m=self.closure[n1][n2]
                    elif self.G[n1][n2]>0 and m<0: m=0
                    for (v1,v2) in [(u,v),(p,q)]:
                        if (v1,v2)==(n1,n2) or (v1,v2)==(n2,n1):
                            if self.closure[v1][v2]>0: n[(v1,v2)]=self.closure[v1][v2]
                            elif self.G[v1][v2]>0: n[(v1,v2)]=0
        maxch=False
        for (n1,n2) in n:
            if n[(n1,n2)]<0:
                res=False
                errs.append("Korak {}: Brid ({},{}) kojeg uklanjate nije dio trenutnog Hamiltonovog ciklusa!".format(step,n1,n2))
            if m==n[(n1,n2)]: maxch=True
        if not maxch:
            res=False
            errs.append("Korak {}: Maksimalni redni broj nadodanog brida u Hamiltonovom ciklusu je {}. Bridovi (u,v)=({},{}) i (p,q)=({},{}) niti jedan nema taj redni broj!".format(step,m,u,v,p,q))
        if self.closure[u][p]>0: n[(u,p)]=self.closure[u][p]
        elif self.G[u][p]>0: n[(u,p)]=0
        if self.closure[v][q]>0: n[(v,q)]=self.closure[v][q]
        elif self.G[v][q]>0: n[(v,q)]=0
        if not self._hasEdge(u,p,self.closure):
            res=False
            errs.append("Korak {}: Brid (u,p)=({},{}) ne postoji u zatvaraču G'".format(step,u,p))
        if self._hasEdge(u,p,Hc,False):
            res=False
            errs.append("Korak {}: Brid (u,p)=({},{}) već postoji u trenutnom Hamiltonovom ciklusu'".format(step,u,p))
        if m<=n[(u,p)]:
            res=False
            errs.append("Korak {}: Brid (u,p)=({},{}) je nadodani i ima viši redni broj ({}) od maksimalno nadodanog brida u trenutnom Hamiltonovom ciklusu ({})'".format(step,u,p,n[(u,p)],m))
        if not self._hasEdge(v,q,self.closure):
            res=False
            errs.append("Korak {}: Brid (v,q)=({},{}) ne postoji u zatvaraču G'".format(step,v,q))
        if self._hasEdge(v,q,Hc,False):
            res=False
            errs.append("Korak {}: Brid (v,q)=({},{}) već postoji u trenutnom Hamiltonovom ciklusu'".format(step,v,q))
        if m<=n[(v,q)]:
            res=False
            errs.append("Korak {}: Brid (v,q)=({},{}) je nadodani i ima viši redni broj ({}) od maksimalno nadodanog brida u trenutnom Hamiltonovom ciklusu ({})'".format(step,v,q,n[(v,q)],m))
        nHcE=None
        if res:
            nHc=deepcopy(Hc)
            nHc[u][v]=nHc[v][u]=0
            nHc[p][q]=nHc[q][p]=0
            nHc[u][p]=nHc[p][u]=1
            nHc[v][q]=nHc[q][v]=1
            nHcE=self._genHcE(nHc)
        return (res,errs,nHcE)
    def isHc(self,HcE:list,chkOrig:bool) -> (bool,list):
        Hc=self._genHc(HcE)
        res,errs=True,[]
        for n in Hc:
            if self._ae(n,Hc)!=2:
                res=False
                errs.append("Vrh {} u trenutnom Hamiltonovom ciklusu nema točno dva priležeća brida!".format(n))
        if chkOrig:
            epairs=[]
            for n1 in Hc:
                for n2 in Hc[n1]:
                    if (n1,n2) not in epairs and Hc[n1][n2]>0 and self.G[n1][n2]==0:
                        epairs.append((n1,n2))
                        epairs.append((n2,n1))
                        res=False
                        errs.append("Brid vašeg Hamiltonovog ciklusa ({},{}) nije sadržan u originalnom grafu!".format(n1,n2))
        start=self.nodes[0]
        self._recIsHc(start,Hc)
        for n1 in Hc:
            for n2 in Hc[n1]:
                if Hc[n1][n2]!=0:
                    res=False
                    errs.append("U slijedu bridova koji ste predali kao Hamiltonov ciklus imate više od jednog ciklusa. Ciklus koji uključuje vrh {} ne sadrži brid ({},{})!".format(start,n1,n2))
        return (res,errs)
    def _recIsHc(self,cn:chr,Hc:dict):
        for an in Hc[cn]:
            if Hc[cn][an]>0:
                Hc[cn][an]=Hc[an][cn]=0
                self._recIsHc(an,Hc)

#bc=BCGraph(['A','B','C','D','E','F','G'])

#bc.addEdges([('A','B'),('A','C'),('A','E'),('B','D'),('B','F'),('B','G'),('C','D'),('D','G'),('E','F'),('E','G')])

#(res,errs)=bc.checkClosure({"1":('B','E'),"2":('B','C'),"3":('C','E'),"4":('C','G'),"5":('C','F'),"6":('D','E'),
#                            "7":('D','F'),"8":('D','A'),"9":('A','F'),"10":('F','G'),"11":('A','G')})
#if not res:
#    for e in errs: print(e)
#else:
#    print("Closure is OK")

#myHC=[('A','B'),('B','C'),('C','D'),('C','E'),('E','F'),('F','G'),('G','A')]
#myHC=[('A','B'),('B','C'),('C','D'),('D','E'),('E','F'),('F','G'),('G','A')]
#(res,errs)=bc.isHc(myHC,False)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Initial HC is correct")

#(res,errs,myHC)=bc.bckStep(1,{"uv":('G','A'),"pq":('B','C')},myHC)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Step 1 is correct: {}".format(myHC))

#(res,errs,myHC)=bc.bckStep(2,{"uv":('F','G'),"pq":('D','E')},myHC)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Step 2 is correct: {}".format(myHC))

#(res,errs,myHC)=bc.bckStep(3,{"uv":('D','F'),"pq":('G','B')},myHC)
#if not res:
#    for e in errs: print(e)
#else:
#    print("Step 3 is correct: {}".format(myHC))

#(res,errs)=bc.isHc(myHC,True)
#if not res:
#    for e in errs: print(e)
#else:
#    print("HC is correct: {}".format(myHC))
