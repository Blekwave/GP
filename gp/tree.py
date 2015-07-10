from copy import deepcopy


class Node(object):
    """A tree's node, with references to its parent, children and its depth."""

    def __init__(self, data, parent):
        """Initializes a new tree node.

        data -- reference to the data stored in the node.
        parent -- reference to the node's parent. (None if root.)"""
        self.data = data
        self.parent = parent
        self.depth = 0 if not parent else parent.depth + 1
        self.children = []

    def __copy__(self):
        """Shallowly copies the node, storing references to data and parent."""
        new = type(self)(self.data, self.parent)
        new.children = self.children
        return new

    def __deepcopy__(self, memo):
        """Performs a deep copy of a node, its data and connected nodes.

        THIS PROCEDURE WILL COPY AN ENTIRE TREE IF ALLOWED TO DO SO."""
        if self.parent not in memo:
            memo[self.parent] = deepcopy(self.parent, memo)
        try:
            if self.data not in memo:
                memo[self.data] = deepcopy(self.data, memo)
            new = type(self)(memo[self.data], memo[self.parent])
        except TypeError:
            new = type(self)(deepcopy(self.data, memo), memo[self.parent])
        new.children = deepcopy(self.children, memo)
        return new

    def update_branch_depth(self, depth):
        """Changes a branch's depthes based on a new value for the root.

        This method is useful for relocating branches, since the depth values
        will be, then, outdated.

        depth -- new depth assigned to the root node of the branch (this)."""

        self.depth = depth
        for child in self.children:
            child.update_branch_depth(depth + 1)


class Tree(object):
    """Regular, generic tree data type."""

    def __init__(self, data=None):
        """Initializes a new tree, optionally creating a root node.

        data -- Data of the root node. If left blank, there will be no root
        node initially."""
        self.nodes = []
        if data:
            self.add_child(data, None)
        else:
            self.root = None

    def add_child(self, data, parent=None):
        """Adds a new child to the tree.

        data -- Data of the new node.
        parent -- New node's parent. If left blank, node is added as root. Will
                  raise an error if a root already exists."""
        if parent is None and self.root is not None:
            raise RuntimeError("Attempt to override a tree's root node.")
        new = Node(data, parent)
        self.nodes.append(new)
        if parent:
            parent.children.append(new)
        else:
            self.root = new
        return new

    def _remove_recursion(self, branch):
        """Recursive procedure called by Tree.remove to traverse the tree."""
        self.nodes.remove(branch)
        for child in branch.children:
            self._remove_recursion(child)

    def remove(self, branch):
        """Removes a branch and all references to it from a tree.

        branch -- root node of the branch to be removed."""

        if branch == self.root:
            self.root = None
        else:
            branch.parent.children.remove(branch)
        self._remove_recursion(branch)

    def __copy__(self):
        """Shallowly copies a tree."""
        new = type(self)()
        new.root = self.root
        new.nodes = self.nodes
        return new

    def __deepcopy__(self, memo):
        """Performs a deep copy of a tree and all its data."""
        new = type(self)()
        if self.root not in memo:
            memo[self.root] = deepcopy(self.root, memo)
        new.root = memo[self.root]
        new.nodes = deepcopy(self.nodes, memo)
        return new
