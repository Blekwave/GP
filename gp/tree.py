import random
from copy import deepcopy

class Node(object):

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = []

    def depth(self):
        depth = 0
        parent = self.parent
        while parent:
            parent = parent.parent
            depth += 1
        return depth

    def __copy__(self):
        new = type(self)(self.data, self.parent)
        new.children = self.children
        return new

    def __deepcopy__(self, memo):
        if not self.parent in memo:
            memo[self.parent] = deepcopy(self.parent, memo)
        try:
            if not self.data in memo:
                memo[self.data] = deepcopy(self.data, memo)
            new = type(self)(memo[self.data], memo[self.parent])
        except TypeError:
            new = type(self)(deepcopy(self.data, memo), memo[self.parent])
        new.children = deepcopy(self.children, memo)
        return new

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

    def remove_recursion(self, branch):
        branch.parent.children.remove(branch)
        self._nodes.remove(branch)
        for child in branch.children:
            self.remove_recursion(child)

    def remove(self, branch):
        if branch == self.root:
            self.root = None
        self.remove_recursion(branch)

    @property
    def root(self):
        return self._root

    @property
    def nodes(self):
        return self._nodes

    def __copy__(self):
        new = type(self)()
        new._root = self._root
        new._nodes = self._nodes
        return new

    def __deepcopy__(self, memo):
        new = type(self)()
        new._nodes = deepcopy(self._nodes, memo)
        if not self._root in memo:
            memo[self._root] = deepcopy(self._root, memo)
        new._root = memo[self._root]
        return new
