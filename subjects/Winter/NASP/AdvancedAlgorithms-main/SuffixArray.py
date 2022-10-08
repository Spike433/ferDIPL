from General import StringPL
from math import floor,log2,ceil
import array

def LinearLCPArray(t: str, A: array) -> (array):
    n = len(t)
    R, H = [0]*n, [0]*n
    for i in range(0, n):
        R[A[i]]=i
    h = 0
    for i in range(0, n):
        if R[i] > 1:
            k = A[R[i]-1]
            while t[i+h] == t[k+h]:
                h = h + 1
            H[R[i]] = h
            if h > 0: h = h - 1
    return H

def CreateLMatrix(n: int, H: array) -> (array):
    lM = [[0]*n for i in range(n)]
    for p in range(0,ceil(log2(n))-1):
        for q in range(0,ceil(n/pow(2,p))-1):
            v1 = q*pow(2,p)
            v2 = min(n, v1 + pow(2,p))
            Hslice=H[v1+1:v2+1]
            lM[v1][v2] = lM[v2][v1] = min(Hslice)
    return lM

class SuffixArray:
    def __init__(self, s: str):
        self.str = StringPL(s, 0, len(s))
        self.n = len(s)
        tmp1 = []
        for i in range(0,len(self.str.s)):
            tmp1.append((i,self.str.clone(i,len(self.str.s)-i)))
        tmp2 = sorted(tmp1,key=lambda x: x[1],reverse=False)
        A, self.SA = [0]*self.n, ['']*self.n
        for i in range(0,self.n):
            A[i]=tmp2[i][0]
            self.SA[i]=tmp2[i][1]
        H = LinearLCPArray(self.str.s, A)
        self.l = CreateLMatrix(self.n, H)

    def search(self, q: str) -> (bool):
        #if q[len(q)-1] != '$': q = q + '$'
        i, j = 0, self.n - 1
        a, b = self.SA[i].lcp(q), self.SA[j].lcp(q)
        if a==len(q) or b==len(q): return True
        return self._searchSA(i, j, a, b, q)
    def _searchSA(self, i: int, j: int, a: int, b: int, q: str) -> (bool):
        if j==i+1: return False
        m = floor((j-(i-1))/2)+i
        if self.l[i][m] < a: return self._searchSA(i,m,a,self.l[i][m],q)
        elif self.l[i][m] > a: return self._searchSA(m,j,a,b,q)
        else:
            sm = self.SA[m]
            for k in range(a,min(len(self.SA[m]),len(q))):
                ch, smk = q[k], sm[k]
                if ch=='$': return True
                if ch < smk: return self._searchSA(i,m,a,k,q)
                elif ch > smk: return self._searchSA(m,j,k,b,q)
                else:
                    if ch!='$' and k==len(q)-1: return True
            return False

class StringArray(SuffixArray):
    def __init__(self, arr): #this is not a suffix array, we cannot use thos fancy linear algorithms
        self.n = len(arr)
        self.SA = arr
        self.l = [[0]*self.n for i in range(self.n)]
        # naive construction of the l-matrix
        for i in range(0,self.n):
            for j in range(i+1,self.n):
                lcp = self.SA[i].lcp(self.SA[j])
                self.l[i][j]=self.l[j][i] = lcp
