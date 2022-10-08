from General import StringPL

class PatriciaTreeNode:
    def __init__(self, str: StringPL, leaf: bool):
        self.str = str
        self.children = [None] * 256 #sigma=ascii
        self.leaf, self.parent = leaf, None
        #self.cno, self.parent = 0, None
    def isLeaf(self) -> (bool):
        return self.leaf
        #return self.cno == 0
    def transition(self, c: chr) -> (object):
        return self.children[ord(c)]
    def insert(self, cnc: object):
        #if self.children[ord(cnc.str.s[cnc.str.p])] is None:
        #    self.cno += 1
        cnc.parent = self
        self.children[ord(cnc.str.s[cnc.str.p])] = cnc
    def remove(self, cnc: object):
        child = self.children[ord(cnc.str.s[cnc.str.p])]
        if child is not None:
            child.parent = None
            #self.cno -= 1
            self.children[ord(cnc.str.s[cnc.str.p])] = None
    def checkChildren(self):
        #if self.cno > 0:
        #    for i in range(0,255):
        #        if self.children[i] is not None:
        #            return (self.cno == 1, self.children[i])
        if not self.leaf:
            for i in range(0,255):
                if self.children[i] is not None:
                    return (self.leaf, self.children[i])
        return (False, None)
    def __str__(self):
        return self.str.substring()


class PatriciaTree:
    def __init__(self):
        self.root = PatriciaTreeNode(StringPL(None, 0, 0), False)
    def search(self, q: str) -> (bool):
        (succ, cn) = self._search(q)
        return succ
    def _search(self, q: str) -> (bool):
        q = q + '$'
        q_p, q_l = 0, len(q)
        sc = 0  # Python starts strings from 0
        cn = self.root
        while not cn.isLeaf():
            cnc = cn.transition(q[sc])
            if cnc is not None:
                t_p, t_l = cnc.str.p, cnc.str.l
                if q[sc:sc + t_l] == cnc.str[0:t_l]:
                    sc, cn = sc + t_l, cnc
                else: return (False, None)
            else: return (False, None)
        return (sc == q_l, cn)
    def insert(self, s: str):
        s = s + '$'
        s_p, s_l = 0, len(s)
        sc = 0 # Python starts strings from 0
        cn = self.root
        while cn==self.root or not cn.isLeaf():
            c = s[sc]
            cnc = cn.transition(c)
            if cnc is not None:
                t_p, t_l = cnc.str.p, cnc.str.l
                if s[sc:sc + t_l] == cnc.str[0:t_l]: #case 3
                    cn,sc=cnc,sc+t_l
                else: #case 2
                    #the first char is always matched
                    for i in range(1, t_l):
                        if s[sc + i] != cnc.str[cnc.str.p + i]: break
                    cnins=PatriciaTreeNode(cnc.str.clone(cnc.str.p, i), False)
                    cnc.str.p,cnc.str.l=cnc.str.p+i,cnc.str.l-i
                    cn.insert(cnins)
                    cnins.insert(cnc)
                    cnleaf=PatriciaTreeNode(StringPL(s, sc + i, s_l - sc - i), True)
                    cnins.insert(cnleaf)
                    return
            else: #case 1
                cnleaf=PatriciaTreeNode(StringPL(s, sc, s_l - sc), True)
                cn.insert(cnleaf)
                return
    def remove(self, s: str):
        (succ, cnleaf) = self._search(s)
        if not succ: return
        os = cnleaf.str.s
        cn = cnleaf.parent
        if cn is not None:
            cn.remove(cnleaf)
            (single, firstChild) = cn.checkChildren()
            if single and cn.parent is not None:
                cnpp = cn.parent
                cnpp.remove(cn)
                firstChild.str.p -= cn.str.l
                firstChild.str.l += cn.str.l
                cnpp.insert(firstChild)
            if firstChild is not None:
                cn = firstChild
                while cn.parent is not None:
                    if cn.parent.str.s == os:
                        cn.parent.str.s = cn.str.s
                    cn = cn.parent
