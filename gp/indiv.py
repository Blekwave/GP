import random

from .tree import Tree
from .var import Var
from copy import deepcopy


class Indiv(object):
    """Tree-structured individual in a GP system."""

    def __init__(self):
        """Initializes a new individual, with an empty tree."""
        self.tree = Tree()

    def _grow_recursion(self, parent, depth, max_depth, primitives, terminals):
        """Recursive call used to generate branches by grow."""
        if depth < max_depth:
            child = self.tree.add_child(random.choice(primitives), parent)
            for i in range(0, child.data.num_args):
                self._grow_recursion(
                    child, depth + 1, max_depth, primitives, terminals)
        else:
            child = self.tree.add_child(random.choice(terminals), parent)

    def grow(self, parent, terminals, functions, max_depth):
        """Randomly generates an individual (or part of it) by grow.

        Grow is a method for individual initialization that randomly adds new
        nodes to a tree from a pool of terminals and functions. If a function
        with parameters is added, children must also be generated, and these
        children may also be functions. The procedure continues until only
        terminals are left as leaves. If the function reaches the last level
        allowed by max_depth, it picks randomly from a pool of only terminals.

        Returns a reference to self.

        parent -- parent of the new branch to be generated.
        terminals -- list of terminal primitives.
        functions -- list of function primitives.
        max_depth -- maximum depth of the branch to be generated."""
        self._grow_recursion(
            parent, 1, max_depth, terminals + functions, terminals)
        return self

    def _eval_recursion(self, parent, variables):
        """Recursive procedure used to traverse the tree and evaluate it."""
        arguments = []  # Stores arguments for the current node, to be computed
        for child in parent.children:
            arguments.append(self._eval_recursion(child, variables))
        if (type(parent.data) is Var):
            return parent.data(variables)
        else:
            return parent.data(*arguments)

    def eval(self, variables=None):
        """Evaluates an individual based on its structure and its variables.

        variables -- dictionary indexed by the individual's variables' labels.
                     Contains each variable's value for this evaluation."""
        return self._eval_recursion(self.tree.root, variables)

    def mutate(self, terminals, functions, depth, max_depth):
        """Mutates an existing individual through grow.

        Two depth values are passed to this function. The smallest one is con-
        sidered, so as not to violate any properties.

        a -- individual to be mutated.
        terminals -- list of terminal primitives.
        functions -- list of function primitives.
        depth -- maximum depth of the branch to be generated.
        max_depth -- maximum depth of an individual after mutation."""
        swap_node = random.choice(self.tree.nodes)
        parent = swap_node.parent
        self.tree.remove(swap_node)
        parent_depth = 0 if not parent else parent.depth
        mutation_depth = min(depth, max_depth - parent_depth - 1)
        self.grow(parent, terminals, functions, mutation_depth)

    def _str_recursion(self, lines, parent, depth):
        """Traverses the tree and computes each node's string, for __str__."""
        lines.append("--" * depth + "> " + str(parent.data))
        for child in parent.children:
            self._str_recursion(lines, child, depth + 1)

    def __str__(self):
        """String representation of the primitive (used for debugging)."""
        lines = []
        self._str_recursion(lines, self.tree.root, 0)
        return "\n".join(lines)

    def __copy__(self):
        """Shallowly copies an individual."""
        new = type(self)()
        new.tree = self.tree
        return new

    def __deepcopy__(self, memo):
        """Performs a deep copy of an individual."""
        new = type(self)()
        if self.tree not in memo:
            memo[self.tree] = deepcopy(self.tree, memo)
        new.tree = memo[self.tree]
        return new


def gather_branch(node, list):
    """Gathers all nodes of a branch in a list.

    node -- node to be added, which may contain children.
    list -- list to which the nodes should be added."""
    list.append(node)
    for child in node.children:
        gather_branch(child, list)


def branch_depth(branch, current_depth=0):
    """Computes the local depth of the deepest node in a branch.

    branch -- current point of the branch being evaluated.
    current_depth -- local depth of the current node. Should be set to 0 or
                     left blank in the initial call."""
    maximum = current_depth
    for child in branch.children:
        maximum = max(maximum, branch_depth(child, current_depth + 1))
    return maximum


def gather_branches_limited(branch, list, max_depth):
    """Gathers all nodes of branches with maximum local depth below max_depth.

    branch -- current branch being evaluated. If its maximum local depth is
              greater or equal to max_depth, its children will be evaluated.
              Otherwise, its children and itself will be added to the list.
    list -- list to which the nodes should be added.
    max_depth -- maximum local depth of the branches to be added to the
                 list."""
    if branch_depth(branch) < max_depth:
        gather_branch(branch, list)
    else:
        for child in branch.children:
            gather_branches_limited(child, list, max_depth)


def swap_branches(tree_a, swap_a, tree_b, swap_b):
    """Swaps two trees' branches, fixing all references accordingly.

    tree_a -- tree to which swap_a belongs.
    swap_a -- branch to be swapped with swap_b.
    tree_b -- tree to which swap_b belongs.
    swap_b -- branch to be swapped with swap_a."""
    swap_a.parent, swap_b.parent = swap_b.parent, swap_a.parent

    if tree_a.root == swap_a:
        tree_a.root = swap_b
        swap_b.update_branch_depth(0)
    else:  # If a node is root, it has no parent
        swap_b.parent.children.remove(swap_a)
        swap_b.parent.children.append(swap_b)
        swap_b.update_branch_depth(swap_b.parent.depth + 1)

    if tree_b.root == swap_b:
        tree_b.root = swap_a
        swap_a.update_branch_depth(0)
    else:
        swap_a.parent.children.remove(swap_b)
        swap_a.parent.children.append(swap_a)
        swap_a.update_branch_depth(swap_a.parent.depth + 1)

    nodes_in_a = []
    gather_branch(swap_a, nodes_in_a)
    nodes_in_b = []
    gather_branch(swap_b, nodes_in_b)

    # Removes references to branches in their previous trees
    for node in nodes_in_a:
        tree_a.nodes.remove(node)
    for node in nodes_in_b:
        tree_b.nodes.remove(node)

    # Adds them to their new trees
    tree_b.nodes.extend(nodes_in_a)
    tree_a.nodes.extend(nodes_in_b)


def crossover(a, b, max_depth):
    """Creates two new individuals by crossover, based on two existing ones.

    a -- individual which will swap a branch with b
    b -- individual which will swap a branch with a
    max_depth -- maximum depth of the new individuals to be generated."""
    new_a, new_b = deepcopy(a), deepcopy(b)
    swap_a = random.choice(new_a.tree.nodes)

    valid_in_b = []
    gather_branches_limited(new_b.tree.root, valid_in_b,
                            max_depth - swap_a.depth - 1)

    swap_b = random.choice(valid_in_b)
    swap_branches(new_a.tree, swap_a, new_b.tree, swap_b)
    return new_a, new_b


def mutation(a, terminals, functions, depth, max_depth):
    """Generates a new individual by mutating an existing one through grow.

    Two depth values are passed to this function. The smallest one is conside-
    red, so as not to violate any properties.

    a -- individual to be mutated.
    terminals -- list of terminal primitives.
    functions -- list of function primitives.
    depth -- maximum depth of the branch to be generated.
    max_depth -- maximum depth of an individual after mutation."""
    new = deepcopy(a)
    new.mutate(terminals, functions, depth, max_depth)
    return new


def reproduction(a):
    """Generates a new individual by reproduction (performs a deep copy)."""
    return deepcopy(a)
