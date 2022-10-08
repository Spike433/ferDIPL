from General import *

def Prim(G,vs):
    MST=NewAdjMatrix(G)
    Vg=[vs]
    Vr=list(G.keys())
    Vr.remove(vs)
    while Vr:
        me=None
        for u in Vg:
            for v in Vr:
                if G[u][v]!=0 and (not me or me[2]>G[u][v]):
                    me=(u,v,G[u][v])
        if me:
            Vg.append(me[1])
            Vr.remove(me[1])
            MST[me[0]][me[1]]=MST[me[1]][me[0]]=G[me[0]][me[1]]
    return MST



