class SWETreeNode:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val

class SWETree:
    def __init__(self, t):
        t.sort(key=lambda i:i[1])
        left = t[:len(t)//2]
        right = t[len(t)//2:]
        # Create root node, and recursively create tree (starting from left)