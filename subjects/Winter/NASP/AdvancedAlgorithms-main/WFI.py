from General import *
import sys

def WFI(G):
    D=G
    P=NewAdjMatrix(G)
    for u in G:
        for v in G:
            if D[u][v]: P[u][v]=u
            if u!=v and D[u][v]==0:
                D[u][v]=sys.maxsize
    for k in G:
        for i in G:
            for j in G:
                if D[i][k]+D[k][j]<D[i][j]:
                    D[i][j]=D[i][k]+D[k][j]
                    P[i][j]=P[k][j]
        print(D)
    return (D,P)
