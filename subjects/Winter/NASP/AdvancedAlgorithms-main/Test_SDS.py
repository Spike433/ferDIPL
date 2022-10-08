import unittest
from Trie import Trie
from PatriciaTree import PatriciaTree
from SuffixArray import SuffixArray,StringArray
from General import StringPL
from SuffixTree import SuffixTree

class SimpleStringCases(unittest.TestCase):
    def test_Trie(self):
        t=Trie()
        t.insert("dado")
        t.insert("da")
        t.insert("dalibor")
        t.insert("ana")
        t.remove("dado")
        self.assertTrue(t.search('dado'))

    def test_PatriciaTree1(self):
        pt=PatriciaTree()
        pt.insert("analisys")
        pt.insert("acronym")
        b1=pt.search('ana')
        pt.insert("analogy")
        pt.insert("acrobat")
        pt.insert("ana")
        self.assertTrue(not b1 and pt.search('ana'))

    def test_PatriciaTree2(self):
        pt=PatriciaTree()
        pt.insert("analisys")
        pt.insert("acronym")
        pt.insert("analogy")
        pt.insert("acrobat")
        pt.insert("ana")
        pt.remove('analisys')
        pt.remove('analogy')
        pt.remove('ana')
        pt.remove('acronym')
        pt.remove('acrobat')
        self.assertTrue(not pt.search('analisys'))

    def test_SuffixArray1(self):
        sa=SuffixArray('banana$')
        res = sa.search('nana$')
        self.assertTrue(res)

    def test_SuffixArray2(self):
        arr = []
        arr.append(StringPL('prognosis$'))
        arr.append(StringPL('programmability$'))
        arr.append(StringPL('programmable$'))
        arr.append(StringPL('programmatic$'))
        arr.append(StringPL('programmatically$'))
        arr.append(StringPL('programmed$'))
        arr.append(StringPL('programmer$'))
        arr.append(StringPL('programmers$'))
        arr.append(StringPL('progress$'))
        arr.append(StringPL('protected$'))
        arr.append(StringPL('protectionism$'))
        arr.append(StringPL('protege$'))
        arr.append(StringPL('protoplasm$'))
        sa=StringArray(arr)
        res = sa.search('protection$')
        self.assertTrue(res)

    def test_SuffixTree1(self):
        st = SuffixTree()
        st.insert('ABABABCDCDE')
        s1 = st.search('BCD')
        s2 = st.search('BCE')
        s3 = st.search('ACD')
        s4 = st.search('DCD')
        self.assertTrue(s1 and not s2 and not s3 and s4)

if __name__ == '__main__':
    unittest.main()
