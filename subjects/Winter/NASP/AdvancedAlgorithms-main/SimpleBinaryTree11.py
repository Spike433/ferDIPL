from typing import Optional


class Node:
    """
    Class representing a single node of a binary tree containing integer values.

    ...

    Attributes
    ----------

    value: int
        Value stored in the node.
    parent: Node, optional
        Parent of the current node. Can be None.
    left: Node, optional
        Left child of the current node. Can be None.
    right: Node, optional
        Right child of the current node. Can be None.
    """

    def __init__(self, value: int) -> None:
        self.value = value
        self.parent = self.right = self.left = None

    def set_left_child(self, node: Optional['Node']) -> None:
        """
        Set the the left child of self to the given node.
        Sets the node's parent to self (if it is not None).

        Args:
            node (Node, optional): the node to set as the child.
        """
        self.left = node
        if node is not None:
            node.parent = self

    def set_right_child(self, node: Optional['Node']) -> None:
        """
        Set the the right child of self to the given node.
        Sets the node's parent to self (if it is not None).

        Args:
            node (Node, optional): the node to set as the child.
        """
        self.right = node
        if node is not None:
            node.parent = self


def left_rotation(node: Node, root: Node) -> Node:
    """Left rotate a node

    Do a left rotation on the node specified as the first argument and return the root
    of the tree. The root can be the specified, second arugment (root) or a new root which
    changed because of the rotation.

    Args:
        node (Node): The node on which the rotation is done.
        root (Node): Root node of the binary tree which contains the node which we are rotating.

    Returns:
        Node: The root of the binary tree, which could have changed due to the rotation.
    """
    rotator = node.right
    new_root = root
    if rotator is None:
        return new_root
    parent = node.parent
    if parent is None:
        root = rotator
        root.parent = None
    else:
        if parent.left is node:
              parent.set_left_child(rotator)
        if parent.right is node:
            parent.set_right_child(rotator)

    t = rotator.left
    rotator.set_left_child(node)
    node.set_right_child(t)

    return new_root

C = self.R
if C is None: return
A = self.P
if A is not None:
    if A.L is self: A.setLeftChild(C)
    if A.R is self: A.setRightChild(C)
else:
    tree.root = C.toRoot()
t = C.L
C.setLeftChild(self)
self.setRightChild(t)


def print_tree(node: Optional[Node], level: int = 0) -> None:
    """
    Prints a rough sketch of the tree in the command line.

    Accepts a node which can be None and prints its right subtree, than its value and then its left subtree, recursivevly.

    Args:
        node (Node, optional): The node for which we are writing out the subtree.
        level (int): Number of empty lines before the actual value - used to discern the tree levels.
    """
    if node is None:
        return
    print_tree(node.right, level + 2)
    print(' ' * level + f'-> {node.value}')
    print_tree(node.left, level + 2)


root = Node(17)
root.left = Node(13)
root.left.left = Node(10)
root.left.right = Node(12)
root.left.right = Node(15)
root.left.right.left = Node(14)
root.right = Node(20)
root.right.left = Node(19)
root.right.right = Node(22)
root.right.left.left = Node(18)

print('Prije rotacije:')
print_tree(root)

# Left rotate around the root (first argument)
root = left_rotation(root, root)

assert root.value == 20
assert root.left.value == 17
assert root.left.left.value == 13
assert root.left.left.left.value == 10
assert root.left.left.right.value == 15
assert root.left.left.right.left.value == 14
assert root.left.right.value == 19
assert root.left.right.left.value == 18
assert root.right.value == 22

print()
print('Nakon rotacije:')
print_tree(root)