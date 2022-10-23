def gen_balanced_tree(sorted_list: Optional[list]) -> Node:
    """
    Generates a balanced binary tree from a ascendingly sorted list of elements.

    Args:
        sorted_list (list, optional): The sorted list of elements.
    
    Returns:
        Node: The root of the generated tree or None if the sorted_list is empty or None.
    """
    # TODO: Implement the tree generation method
    n=len(sorted_list)
    if n>0:
        i=math.floor(n/2)+(n % 2)
        root=Node(sorted_list[i-1])
        root.set_left_child(gen_balanced_tree(sorted_list[0:i-1]))
        root.set_right_child(gen_balanced_tree(sorted_list[i:n]))
        return root
    else: return None