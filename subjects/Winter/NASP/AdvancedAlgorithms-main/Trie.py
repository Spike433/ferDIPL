class TrieNode:
    def __init__(self, p=None):
        self.children = [None] * 256 #sigma=ascii
        self.parent, self.cno = p, 0
    def isLeaf(self) -> (bool):
        return self.cno == 0
    def transition(self, c: chr) -> (object):
        return self.children[ord(c)]
    def insert(self, c: chr) -> (object):
        cn = self.transition(c)
        if cn is None:
            ncn = TrieNode(self)
            self.children[ord(c)] = ncn
            self.cno += 1
            return ncn
        else: return cn
    def remove(self, c: chr) -> (bool):
        cn = self.transition(c)
        if cn is not None:
            self.children[ord(c)] = None
            self.cno -= 1
            return True
        return False
    def __str__(self):
        s = 'Children(' + str(self.cno) + '):'
        for i in range(0,256):
            if(self.children[i] is not None):
                s+=' '+chr(i)
        return s

class Trie:
    def __init__(self):
        self.root = TrieNode(None)
    def insert(self, s: str):
        currTN = self.root
        for c in s:
            currTN = currTN.insert(c)
        currTN.insert('$')
    def search(self, q: str) -> (bool, TrieNode):
        currTN = self.root
        for c in q + '$':
            currNTN = currTN.transition(c)
            if currNTN is None: return (False, currTN)
            currTN = currNTN
        return (currTN.isLeaf(), currTN)
    def remove(self, s: str) -> (bool):
        (res, ltn) = self.search(s)
        if res:
            s = '$' + "".join(reversed(s))
            currTN = ltn.parent
            for c in s:
                split = len(currTN.children) > 1
                currTN.remove(c)
                if split: break
                currTN = currTN.parent
                if currTN is None: break  # we are at the root node
            return True
        return False
