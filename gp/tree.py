class Node(object):

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = []

class Tree(object):

    def __init__(self, data=None):
        self._nodes = []
        if data:
            self.add_child(data, None)
        else: 
            self._root = None

    def add_child(self, data, parent=None):
        new = Node(data, parent)
        self._nodes.append(new)
        if parent:
            parent.children.append(new)
        else:
            self._root = new
        return new

    @property
    def root(self):
        return self._root

    @property
    def nodes(self):
        return self._nodes
