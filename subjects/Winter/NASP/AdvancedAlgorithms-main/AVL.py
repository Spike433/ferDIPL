from SimpleBinaryTree import SimpleBinaryTree,Node

class AVLTree(SimpleBinaryTree):
    def updateHeights(self,l):
        for n in l:
            n.updateHeight()
    def AVLDetectRotate(self,n):
        if n.bal_factor()==2:
            n1=n.R
            n1bf=n1.bal_factor()
            if n1 is not None and n1bf in [0,1]:
                n.leftrotate(self)
                self.updateHeights([n,n1])
            elif n1 is not None and n1bf==-1:
                n1.rightrotate(self)
                n.leftrotate(self)
                self.updateHeights([n1,n,n.P])
        else:
            n1=n.L
            n1bf=n1.bal_factor()
            if n1 is not None and n1bf in [0,-1]:
                n.rightrotate(self)
                self.updateHeights([n,n1])
            elif n1 is not None and n1bf==1:
                n1.leftrotate(self)
                n.rightrotate(self)
                self.updateHeights([n,n1,n.P])

    def AVLBalance(self,n):
        n.updateHeight()
        p=n.P
        if n.bal_factor() in [-2,2]:
            self.AVLDetectRotate(n)
        if p is not None:
            self.AVLBalance(p)

    def insert(self,v):
        n=super().insert(v)
        if n is not None:
            self.AVLBalance(n)
    def remove(self,v):
        n=super().remove(v)
        if n is not None:
            self.AVLBalance(n)
