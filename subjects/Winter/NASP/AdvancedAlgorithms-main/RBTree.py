from SimpleBinaryTree import SimpleBinaryTree

class RBTree(SimpleBinaryTree):
    def insertRestructure(self,n):
        if n.P is None: return
        P,G=n.P,None
        if P is not None: G=P.P
        while P is not None and G is not None and P.color=='red':
            if P==G.L:
                case='LL'
                if n==P.R:
                    case='LR'
                U=G.R
            else:
                case='RR'
                if n==P.L:
                    case='RL'
                U=G.L
            if U is not None and U.color=='red':
                P.color=U.color='black'
                G.color='red'
                n=G
            else:
                if case in ['LL','RR']:
                    if case=='LL':
                        G.rightrotate(self)
                    else:
                        G.leftrotate(self)
                    tmp=P.color
                    P.color=G.color
                    G.color=tmp
                else:
                    if case=='LR':
                        P.rightrotate(self)
                    else:
                        P.leftrotate(self)
                    n=P
            P,G=n.P,None
            if P is not None: G=P.P
        self.root.color='black'
    def insert(self,v):
        p=super().insert(v)
        if p is None:
            n=self.root
        else:
            if p.L is not None and p.L.S==v: n=p.L
            else: n=p.R
        n.color='red'
        self.insertRestructure(n)
