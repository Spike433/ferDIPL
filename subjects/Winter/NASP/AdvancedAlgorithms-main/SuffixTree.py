from General import StringPL
from PatriciaTree import PatriciaTreeNode

class SuffixTreeNode(PatriciaTreeNode):
    def __init__(self, str: StringPL, leaf: bool):
        self.str = str
        self.children = [None] * 256 #sigma=ascii
        self.leaf, self.parent = leaf, None
        self.suffixLink = None

class SuffixTree:
    def __init__(self):
        self.root = SuffixTreeNode(StringPL(None, 0, 0), False)
    def search(self, q: str) -> (bool):
        (succ, cn) = self._search(q)
        return succ
    def _search(self, q: str) -> (bool):
        q_p, q_l = 0, len(q)
        sc = 0  # Python starts strings from 0
        cn = self.root
        while not cn.isLeaf():
            cnc = cn.transition(q[sc])
            if cnc is not None:
                t_p, t_l = cnc.str.p, cnc.str.l
                minlen = min(t_l,len(q)-sc)
                x1, x2 = q[sc:sc + minlen], cnc.str[0:t_l]
                if x1 == x2:
                    sc, cn = sc + t_l, cnc
                else:
                    for i in range(1, minlen):
                        if q[sc + i] != cnc.str[i]: return (False, None)
                    return (True, None)
            else: return (False, None)
        return (sc == q_l, cn)
    def insert(self, s: str): # implementation of the Ukkonen's algorithm
        spl = StringPL(s)
        for i in range(0,len(spl)):
            self._insert1(spl.clone(0, i), spl[i])
    def _insert1(self, prefix: StringPL, cins: chr):
        self.lastChar, self.lastTransChar, self.skipNodes, self.lastInternal = -1, -2, set(), None
        for pi in range(0, len(prefix)):
            if pi > self.lastTransChar:
                self._insert2(prefix.clone(pi, len(prefix)-pi), cins, False)
        self._insert2(StringPL(cins), cins, True)
    def _insert2(self, s: StringPL, cins: chr, noPrefix: bool):
        cns = []
        scb = 0
        if self.lastChar >= s.p and not noPrefix:
            for cn in self.skipNodes: cns.append(cn)
            scb = self.lastChar - s.p
            self.lastTransChar = self.lastChar
        else: cns.append(self.root)
        for cn1 in cns:
            cn = cn1
            sc = scb
            while cn==self.root or not cn.isLeaf():
                c = s[sc]
                cnc = cn.transition(c)
                if cnc is not None:
                    if noPrefix: return
                    t_p, t_l = cnc.str.p, cnc.str.l
                    minlen = min(t_l,len(s)-sc)
                    if s[sc:sc + minlen] == cnc.str[0:t_l]:
                        cn,sc=cnc,sc+t_l
                        if cn.isLeaf():
                            cn.str.append(cins)
                            break
                        else:
                            sn = cn
                            if sn.suffixLink is not None and self.lastChar < sc:
                                self.lastChar = sc + s.p
                                while sn.suffixLink is not None:
                                    self.skipNodes.add(sn)
                                    sn = sn.suffixLink
                                self.skipNodes.add(sn)
                    else:
                        i = 0
                        for i in range(1, minlen):
                            if s[sc + i] != cnc.str[i]: raise s + ' cannot be found in the Suffix Tree'
                        if cnc.str[i+1] != cins:
                            cnins=SuffixTreeNode(cnc.str.clone(cnc.str.p, i+1), False)
                            cnc.str.p,cnc.str.l=cnc.str.p+(i+1),cnc.str.l-(i+1)
                            cn.insert(cnins)
                            cnins.insert(cnc)
                            cnleaf=SuffixTreeNode(StringPL(cins), True)
                            cnins.insert(cnleaf)
                            if self.lastInternal is not None:
                                self.lastInternal.suffixLink = cnins
                            if len(cnins.str)==1: cnins.suffixLink = self.root
                            elif len(cnins.str)>1: self.lastInternal = cnins
                        break
                else:
                    cnleaf=SuffixTreeNode(StringPL(s.s, sc, s.l - sc), True)
                    cn.insert(cnleaf)
                    break
