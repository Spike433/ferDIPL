from statistics import median
from random import uniform


def is_in_range(q1: float, q2: float, value: float) -> bool:
    """
    Function return true if the value is in ranges between two points.
    Args:
        q1 (float): The first coordinate.
        q2 (float): The second coordinate.
        value (float): The value that does (not) fall between point.
    Returns:
        bool: If the value falls in range between the two points.
    """
    if q1 is not None and q2 is not None and q1 <= value <= q2:
        return True
    elif q1 is None and q2 is not None and value <= q2:
        return True
    elif q1 is not None and q2 is None and q1 <= value:
        return True
    return False


def is_in_window(point: tuple, qx1: float, qx2: float, qy1: float, qy2: float) -> bool:
    """
    Function return true if point in 2-dimensional space belongs to the window.
    Args:
        point (Tuple): Point in space represented by x and y coordinates.
        qx1 (float): First x-coordinate of the window.
        qx2 (float): Second x-coordinate of the window.
        qy1 (float): First y-coordinate of the window.
        qy2 (float): Second y-coordinate of the window.
    Returns:
        bool: True if point belong to the window, else false.
    """
    return is_in_range(qx1, qx2, point[0]) and is_in_range(qy1, qy2, point[1])


class IntervalNode:
    """
    Class representing interval node.
    ...
    Properties
    ----------
    x_median: float
        Median of the x values.
    left_child: IntervalNode
        Left child of the tree.
    right_child: IntervalNode
        Right child of the tree.
    intervals: List
        The list of intervals.
    tree_left: List
        Left tree.
    tree_right: List
        Right tree.

    """

    def __init__(self, x_median: float) -> None:
        self.x_median = x_median
        self.left_child, self.right_child = None, None
        self.intervals = []
        self.tree_left, self.tree_right = [], []

    def __str__(self) -> str:
        """
        Format interval node - override to string method.
        Returns:
            str: Formatted string.
        """
        return "|{}|{}".format(self.x_median, self.intervals)


class IntervalTree:
    """
    Class representing the format tree.
    ...
    Properties
    ----------
    root_node: IntervalNode
        The root of the tree.
    """

    def __init__(self, interval_list: list) -> None:
        self.root_node = self._create(interval_list)

    def _create(self, interval_list: list) -> IntervalNode:
        """
        Method for creating tree from the interval list.
        Args:
            interval_list (list): List of intervals.
        Returns:
            IntervalNode: Root node of the created tree.
        """
        if len(interval_list) == 0:
            return None
        else:
            epoints = set(map(lambda si: si[0][0], interval_list)).union(
                set(map(lambda si: si[0][1], interval_list)))
            x_median = median(epoints)
            node = IntervalNode(x_median)
            interval_left = list(
                filter(lambda si: si[0][0] < x_median and si[0][1] < x_median, interval_list))
            interval_right = list(
                filter(lambda si: si[0][0] > x_median and si[0][1] > x_median, interval_list))
            interval_medians = list(
                filter(lambda si: si not in interval_left + interval_right, interval_list))
            node.intervals = interval_medians
            node_left, node_right = self._create(
                interval_left), self._create(interval_right)
            node.left_child, node.right_child = node_left, node_right
            if len(interval_medians) > 0:
                node.tree_left += list(map(lambda si: {'point': (
                    min(si[0][0], si[0][1]), si[1]), 'interval': si}, interval_medians))
                node.tree_right += list(map(lambda si: {'point': (
                    max(si[0][0], si[0][1]), si[1]), 'interval': si}, interval_medians))
            return node

    def query(self, qx1: float, qx2: float, qy1: float, qy2: float) -> list:
        """
        Helper method to query the tree.
        Args:
            qx1 (float): First x-coordinate of the window.
            qx2 (float): Second x-coordinate of the window.
            qy1 (float): First y-coordinate of the window.
            qy2 (float): Second y-coordinate of the window.
        Returns:
            list: List of nodes within the window.
        """
        if self.root_node is not None:
            return self._query(self.root_node, qx1, qx2, qy1, qy2)
        else:
            return []

    def _query(self, node: IntervalNode, qx1: float, qx2: float, qy1: float, qy2: float) -> list:
        """
        Main method to query the tree.
        Args:
            node (IntervalNode): Root node of the tree.
            qx1 (float): First x-coordinate of the window.
            qx2 (float): Second x-coordinate of the window.
            qy1 (float): First y-coordinate of the window.
            qy2 (float): Second y-coordinate of the window.
        Returns:
            list: List of nodes within the window.
        """
        pom, bool_var = set(), None
        if is_in_range(qx1, qx2, node.x_median):
            for tmp in node.tree_right:
                if is_in_window(tmp["point"], qx1, None, qy1, qy2):
                    pom.add(tmp['interval'])
            for tmp in node.tree_left:
                if is_in_window(tmp["point"], None, qx2, qy1, qy2):
                    pom.add(tmp['interval'])
            bool_var = 'both'
        elif qx1 is not None and node.x_median < qx1:
            for tmp in node.tree_right:
                if is_in_window(tmp["point"], qx1, None, qy1, qy2):
                    pom.add(tmp['interval'])
            bool_var = 'right'
        elif qx2 is not None and node.x_median > qx2:
            for tmp in node.tree_left:
                if is_in_window(tmp["point"], None, qx2, qy1, qy2):
                    pom.add(tmp['interval'])
            bool_var = 'left'
        if bool_var in ['both', 'left'] and node.left_child is not None:
            pom = pom.union(self._query(node.left_child, qx1, qx2, qy1, qy2))
        if bool_var in ['both', 'right'] and node.right_child is not None:
            pom = pom.union(self._query(node.right_child, qx1, qx2, qy1, qy2))
        return list(pom)

    def __str__(self) -> str:
        """
        Format interval node - override to string method.
        Returns:
            str: Formatted string.
        """
        res, q = "", [self.root_node, "\n"]
        while q != ["\n"]:
            n = q[0]
            q = q[1:]
            if type(n) is str:
                res += n
                q.append("\n")
            else:
                res += "*"
                if n.left_child:
                    res += "L"
                    q.append(n.left_child)
                res += str(n)
                if n.right_child:
                    q.append(n.right_child)
                    res += "R"
                res += "*"
        return res
