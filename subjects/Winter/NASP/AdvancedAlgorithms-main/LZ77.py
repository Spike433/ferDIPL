from random import randint
from math import ceil,floor

# Rabin Karp Algorithm
def rk(pat, txt, q = 101, d = 256):
	M,N,i,j,p,t,h = len(pat),len(txt),0,0,0,0,1
	res = []
	for i in range(M-1):
		h = (h*d)%q
	for i in range(M):
		p = (d*p + ord(pat[i]))%q
		t = (d*t + ord(txt[i]))%q
	for i in range(N-M+1):
		if p==t:
			for j in range(M):
				if txt[i+j] != pat[j]:
					break
				else: j+=1
			if j==M:
				res.append(i)
		if i < N-M:
			t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q
			if t < 0:
				t = t+q
	return res

def searchString(D:list, L:list, Ld:int=4) -> (int, int):
	for j in range(len(L),0,-1):
		r1=rk(L[0:j],D+L)
		r2=list(filter(lambda x: x<Ld, r1))
		if len(r2)>0:
			i=(Ld-1)-max(r2)
			return (i,j)
	return (-1,-1)


def LZ77Encode(I:str, Ld:int=4, La:int=4) -> list:
	# init
	L,I=I[:La],I[La:]
	D=L[0]*Ld
	res=[]
	res.append(L[0])
	while len(L)>0:
		(i,j)=searchString(D,L,Ld)
		if i==-1:
			i,j,k=0,0,L[0]
		else:
			if j==len(L): j,k=j-1,L[-1]
			else: k=L[j]
		res.append((i,j,k))
		T=D+L+I
		D=T[j+1:j+1+Ld]
		L=T[j+1+Ld:j+1+Ld+La]
		I=T[j+1+Ld+La:]
	return res

def LZ77Decode(E:list, Ld:int=4, La:int=4) -> str:
	D,L,res=E[0]*Ld,"",""
	for (i,j,k) in E[1:]:
		B=D+L
		so=j/(i+1)
		t=B[Ld-(i+1):Ld-(i+1)+j]
		W=t
		if so>1:
			for z in range(floor(so-1)): W+=t
			rest=j%(i+1)
			for z in range(rest): W+=t[z]
		W+=k
		res+=W
		B+=W
		D,L=B[len(W):Ld+len(W)],""
	return res

def generateTest() -> str:
	names=["Dalibor","Mihael","Mario","Sonja","Tomislav","Vedran","Kreso"]
	total=randint(10,20)
	res=""
	for i in range(total):
		s1=names[randint(0,len(names)-1)]
		inc=True if randint(0,1)==1 else False
		if inc:
			s2=names[randint(0,len(names)-1)]
			j=randint(0,len(s1)-1)
			s1=s1[:j]+s2+s1[j:]
		res+=s1
	return res

def testCompressedSequence(r:list) -> (bool,list):
	rb,rl=True,[]
	if type(r[0])!=str:
		rb=False
		rl.append("First element must be a character")
	i=1
	for trip in r[1:]:
		if type(trip)!=tuple or len(trip)!=3:
			rb=False
			rl.append("List element {} is not a triplet".format(i))
		else:
			if type(trip[0])!=int:
				rb=False
				rl.append("Triplet {}, element i is not a number".format(i))
			if type(trip[1])!=int:
				rb=False
				rl.append("Triplet {}, element j is not a number".format(i))
			if type(trip[2])!=str:
				rb=False
				rl.append("Triplet {}, element k is not a string".format(i))
		i+=1
	return (rb,rl)
