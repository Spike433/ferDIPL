from math import ceil,log,floor,pow

def DSW_rotates(tree,rcount):
    node,A=tree.root,None
    while rcount>0:
        A1=node.R
        node.leftrotate(tree)
        rcount=rcount-1
        A=A1
        node=A.R

def DSW(tree,n):
    if tree.root is None: return
    tree.rightbackbone()
    h=ceil(log(n+1,2))
    i=pow(2,h-1)-1
    DSW_rotates(tree,n-i)
    while i>1:
        i=floor(i/2)
        DSW_rotates(tree,i)

