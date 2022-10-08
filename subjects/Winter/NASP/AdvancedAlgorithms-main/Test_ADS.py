import unittest
from SimpleBinaryTree import SimpleBinaryTree,Node
from CreateBalancedBinaryTree import CreateBalBT
from DSW import DSW
from AVL import AVLTree
from BTree import BTree
from BTreeList import BTreeList,testNode
from RBTree import RBTree
from BinaryTree import BinaryTree,NodeValue
from Lists import List
from SkipLists import SkipList

class SimpleBinaryTreeCases(unittest.TestCase):
    def test_BinaryTree(self):
        bt=BinaryTree()
        bt.insert(NodeValue(10))
        bt.insert(NodeValue(4))
        bt.insert(NodeValue(7))
        bt.insert(NodeValue(1))
        bt.insert(NodeValue(15))
        bt.insert(NodeValue(17))
        bt.insert(NodeValue(12))
        bt.remove(NodeValue(10))

    def test_SimpleBinaryTree(self):
        bt=SimpleBinaryTree()
        bt.insert(10)
        bt.insert(6)
        bt.insert(4)
        bt.insert(9)
        bt.insert(16)
        bt.insert(19)
        bt.insert(11)
        self.assertIs(bt.query(11) is not None,bt.query(12) is None)

    def test_RemoveSimpleBinaryTree(self):
        bt=SimpleBinaryTree()
        bt.root=Node(14)
        bt.root.setLeftChild(Node(6))
        bt.root.setRightChild(Node(21))
        bt.root.L.setLeftChild(Node(4))
        bt.root.L.setRightChild(Node(11))
        bt.root.L.R.setLeftChild(Node(9))
        bt.root.L.R.setRightChild(Node(12))
        bt.root.R.setLeftChild(Node(15))
        bt.root.R.setRightChild(Node(25))
        bt.root.R.L.setRightChild(Node(17))
        bt.root.R.L.R.setLeftChild(Node(16))
        bt.remove(21)
        self.assertTrue(bt.query(21) is None)

    def test_CreateBalancedBinaryTree(self):
        V=[3,7,1,15,11,21,24,14,9,19]
        Vs=sorted(V)
        bt=SimpleBinaryTree(CreateBalBT(Vs))
        self.assertTrue(bt.query(11) is not None)

    def test_CreateRightBackbone(self):
        V=[3,7,1,15,11,21,24,14,9,19]
        Vs=sorted(V)
        bt=SimpleBinaryTree(CreateBalBT(Vs))
        bt.rightbackbone()
        self.assertTrue(bt.query(11) is not None)

    def test_DSW1(self):
        bt=SimpleBinaryTree()
        bt.insert(3)
        bt.insert(7)
        bt.insert(1)
        bt.insert(15)
        bt.insert(11)
        bt.insert(21)
        bt.insert(24)
        bt.insert(14)
        bt.insert(9)
        bt.insert(19)
        DSW(bt,bt.nodes())
        self.assertTrue(bt.isBalanced())

    def test_AVL1(self):
        bt=SimpleBinaryTree()
        bt.insert(15)
        bt.insert(6)
        bt.insert(21)
        bt.insert(18)
        bt.insert(25)
        avlt=AVLTree(bt.root)
        avlt.insert(19)
        self.assertTrue(avlt.isBalanced())

    def test_AVL2(self):
        avlt=AVLTree()
        avlt.insert(16)
        avlt.insert(29)
        avlt.insert(18)
        avlt.insert(34)
        avlt.insert(26)
        avlt.insert(15)
        avlt.insert(45)
        avlt.insert(33)
        avlt.insert(6)
        avlt.insert(37)
        avlt.insert(49)
        avlt.insert(48)
        avlt.insert(40)
        avlt.remove(16)
        avlt.remove(45)
        avlt.remove(37)
        self.assertTrue(avlt.isBalanced())

    def test_BTree1(self):
        bt=BTree(16,deg=4)
        bt.insert([29, 18, 34, 26, 15, 45, 33, 6, 37, 49, 48, 40])
        bt.remove(16)
        bt.remove(45)
        bt.remove(33)
        bt.remove([37,48])
        bt.remove(49)
        bt.remove(26)
        bt.remove(18)
        bt.remove([15,40])
        bt.remove(6)
        self.assertTrue(bt.search(29) is not None and bt.search(6) is None)

    def test_BTree2(self):
        bt=BTreeList(16,deg=4)
        bt.insertValues([29, 18, 34, 26, 15, 45, 33, 6, 37, 49, 48, 40])
        bt.removeValue(16)
        bt.removeValue(45)
        bt.removeValue(33)
        bt.removeValues([37,48])
        bt.removeValue(49)
        bt.removeValue(26)
        bt.removeValue(18)
        bt.removeValues([15,40])
        bt.removeValue(6)
        self.assertTrue(bt.searchValue(29) and not bt.searchValue(6))

    def test_RB1(self):
        rbt=RBTree()
        rbt.insert(16)
        rbt.insert(29)
        rbt.insert(18)
        rbt.insert(34)
        rbt.insert(26)
        rbt.insert(15)
        rbt.insert(45)
        rbt.insert(33)
        rbt.insert(6)
        rbt.insert(37)
        rbt.insert(49)
        rbt.insert(48)
        rbt.insert(40)
        self.assertIs(rbt.root.S==29,rbt.root.color=='black','The root node should be 29-black')
        self.assertIs(rbt.root.R.S==34,rbt.root.R.color=='black','The 1st right node should be 34-black')
        self.assertIs(rbt.root.R.R.S==45,rbt.root.R.R.color=='red','The second right node should be 45-red')
        self.assertIs(rbt.root.R.R.R.S==49,rbt.root.R.R.R.color=='black','The 3rd right node should be 49-black')
        self.assertIs(rbt.root.R.R.R.L.S==48,rbt.root.R.R.R.L.color=='red','The tested leaf should be 48-red')

    def test_Lists(self):
        l=List()
        l.insert(7)
        l.insert(1)
        l.insert(12)
        l.insert(5)
        l.insert(6)
        l.insert(6)
        l.insert(21)
        l.insert(2)
        s1=l.search(7)
        s2=l.search(11)
        s3=l.search(6)

    def test_SkipList(self):
        l=SkipList()
        l.insert(7)
        l.insert(1)
        l.insert(12)
        l.insert(5)
        l.insert(6)
        l.insert(6)
        l.insert(21)
        l.insert(2)
        l.insert(15)
        l.insert(11)
        l.insert(9)
        l.insert(17)
        s1=l.search(7)
        s2=l.search(11)
        s3=l.search(6)
        l.remove(6)
        l.remove(11)

if __name__ == '__main__':
    unittest.main()
