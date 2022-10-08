from SimpleBinaryTree import Node

def CreateBalBT(Vs):
    n=len(Vs)
    if n>0:
        i=(n // 2)+(n % 2)
        root=Node(Vs[i-1])
        root.setLeftChild(CreateBalBT(Vs[0:i-1]))
        root.setRightChild(CreateBalBT(Vs[i:n]))
        return root
    else: return None
