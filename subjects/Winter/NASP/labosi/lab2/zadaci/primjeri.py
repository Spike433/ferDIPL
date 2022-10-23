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

# Right rotate around the root (first argument)
root = right_rotation(root, root)

assert root.value == 13
assert root.left.value == 10
assert root.right.value == 17
assert root.right.left.value == 15
assert root.right.left.left.value == 14
assert root.right.right.value == 20
assert root.right.right.left.value == 19
assert root.right.right.left.left.value == 18
assert root.right.right.right.value == 22

print()
print('Nakon rotacije:')
print_tree(root)