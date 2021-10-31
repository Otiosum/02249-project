import copy

class SWETreeNode:
    def __init__(self, parent, depth, values):
        self.left = None
        self.right = None
        self.parent = parent

        # Node metadata
        self.depth = depth
        self.values = values
        self.weight = sum(len(j) for i, j in self.values)

        # Node useful data
        self.node_t = set()
        self.node_candidates = {}
        self.node_candidates_intersect = {}
        self.node_candidates_rem = []

        for v in values:
            self.node_t.add(v[0])
            self.node_candidates[v[0]] = copy.deepcopy(v[1])
            self.node_candidates_intersect[v[0]] = []

class SWETree:
    def __init__(self, tuples):
        items = []
        for t in tuples:
            items.append((t, tuples[t]))

        items.sort(key=lambda i:i[1])
        left = items[:len(items)//2]
        right = items[len(items)//2:]

        self.root_node = SWETreeNode(None, 0, items)
        self.root_node.left = self.create_next_node(self.root_node, 1, left)
        self.root_node.right = self.create_next_node(self.root_node, 1, right)

    def create_next_node(self, parent, depth, values):
        node = SWETreeNode(parent, depth, values)

        if len(values) > 1:
            child_left = values[:-(-len(values)//2)]
            child_right = values[-(-len(values)//2):]

            node.left = self.create_next_node(node, depth + 1, child_left)
            node.right = self.create_next_node(node, depth + 1, child_right)

        return node

    def print_tree(self):
        self.print_next_node(self.root_node)

    def print_next_node(self, current : SWETreeNode):
        if current.left is not None:
            print("L > ", end='')
            self.print_next_node(current.left)
        if current.right is not None:
            print("R > ", end='')
            self.print_next_node(current.right)

        print("")
        print("D: {}, W: {}, Vals: ".format(current.depth, current.weight))
