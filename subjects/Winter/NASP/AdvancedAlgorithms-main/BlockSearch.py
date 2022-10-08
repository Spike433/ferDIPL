import collections

def BlockSearch(G):
    blocks=[]
    for v in G:
        G[v]['n'] = G[v]['p'] = 0
    step = 0
    S = collections.deque()
    for u in G:
        if (G[u]['n']==0):
            BlockSearch_recursive(G,u,step,S,blocks)
    return blocks


def BlockSearch_recursive(G,u,step,S,blocks):
    G[u]['p'] = G[u]['n'] = step = step+1
    for v in G[u]['adj']:
        if (G[v]['n']==0):
            if((u,v) not in S and (v,u) not in S):
                S.append((u,v))
            BlockSearch_recursive(G,v,step,S,blocks)
            if(G[v]['p']>=G[u]['n']):
                b = []
                e = S[-1]
                while(e!=(u,v) and e!=(v,u)):
                    b.append(S.pop())
                    e = S[-1]
                b.append(S.pop())
                blocks.append(b)
            else:
                G[u]['p'] = min(G[u]['p'],G[v]['p'])
        elif (len(S)>0 and (v,u)!=S[-1]):
            G[u]['p'] = min(G[u]['p'],G[v]['n'])


