import collections

def SCCSearch(G):
    for v in G:
        G[v]['n']=G[v]['p']=0
    step=0
    S=collections.deque()
    res=[]
    for u in G:
        if (G[u]['n']==0):
            SCCSearch_r(G,u,step,S,res)
    return res

def SCCSearch_r(G,u,step,S,res):
    G[u]['p']=G[u]['n']=step
    step=step+1
    S.append(u)
    for v in G[u]['adj']:
        if (G[v]['n']==0):
            SCCSearch_r(G,v,step,S,res)
            G[u]['p']=min(G[u]['p'],
                          G[v]['p'])
        elif (G[v]['n']<G[u]['n']):
            G[u]['p']=min(G[u]['p'],
                          G[v]['n'])
    if (G[u]['p']==G[u]['n']):
        scc=[]
        vx=S[-1]
        while(vx!=u):
            scc.append(S.pop())
            vx=S[-1]
        scc.append(S.pop())
        res.append(scc)


