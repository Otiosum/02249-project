class SWETreeNode:
    def __init__(self, parent, depth, values):
        self.parent = parent
        self.depth = depth
        self.values = values
        self.weight = sum(j for i, j in self.values)
        self.left = None
        self.right = None

class SWETree:
    def __init__(self, tuples):
        items = []
        for t in tuples:
            items.append((t, len(tuples[t])))

        items.sort(key=lambda i:i[1])
        left = items[:len(items)//2]
        right = items[len(items)//2:]

        self.root_node = SWETreeNode(None, 0, items)
        self.root_node.left = self.create_next_node(self.root_node, 1, left)
        self.root_node.right = self.create_next_node(self.root_node, 1, right)

    def create_next_node(self, parent, depth, values):
        # Create node
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
        print("D: {}, W: {}, Vals: ".format(current.depth, current.weight), end='')
        print(current.values)
