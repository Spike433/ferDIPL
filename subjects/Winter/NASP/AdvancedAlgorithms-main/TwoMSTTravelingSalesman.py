from Dijkstra import DijkstraMSTUndirected
from EulerianCircuits import Eulerization, Hierholzer, Fleury
from Kruskal import KruskalUndirected
import copy

def TwoMSTTSP(G,s):
    #Gmst=DijkstraMSTUndirected(copy.deepcopy(G))
    Gmst=KruskalUndirected(copy.deepcopy(G))
    GEmst=Eulerization(Gmst)
    Ce=Hierholzer(GEmst,s)
    #Ce=Fleury(GEmst,s) #we cannot use Fleury here, as it uses the BlockSearch algorithm that does not work with
                        #undirected multigraphs
    v=[s]
    for e in Ce:
        if e[1] not in v and G[v[-1]][e[1]]>0:
            v.append(e[1])
    Ch=[]
    if len(v)>=2:
        for i in range(len(v)-1):
            Ch.append(((v[i],v[i+1]),G[v[i]][v[i+1]]))
        Ch.append(((v[-1],v[0]),G[v[-1]][v[0]]))
    return Ch

