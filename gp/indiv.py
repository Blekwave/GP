import random

from tree import Tree
from var import Var
from copy import deepcopy


class Indiv(object):

    def __init__(self):
        self.tree = Tree()

    def grow_recursion(self, parent, depth, max_depth, primitives, terminals):
        if depth < max_depth:
            child = self.tree.add_child(random.choice(primitives), parent)
            for i in range(0, child.data.num_args):
                self.grow_recursion(
                    child, depth + 1, max_depth, primitives, terminals)
        else:
            child = self.tree.add_child(random.choice(terminals), parent)

    def grow(self, parent, terminals, functions, max_depth):
        self.grow_recursion(
            parent, 1, max_depth, terminals + functions, terminals)

    def eval_recursion(self, parent, variables):
        arguments = []
        for child in parent.children:
            arguments.append(self.eval_recursion(child, variables))
        if (type(parent.data) is Var):
            return parent.data(variables)
        else:
            return parent.data(*arguments)

    def eval(self, variables=None):
        return self.eval_recursion(self.tree.root, variables)

    def _str_recursion(self, lines, parent, depth):
        lines.append("--" * depth + "> " + str(parent.data))
        for child in parent.children:
            self._str_recursion(lines, child, depth + 1)

    def __str__(self):
        lines = []
        self._str_recursion(lines, self.tree.root, 0)
        return "\n".join(lines)

    def __copy__(self):
        new = type(self)()
        new.tree = self.tree
        return new

    def __deepcopy__(self, memo):
        new = type(self)()
        if self.tree not in memo:
            memo[self.tree] = deepcopy(self.tree, memo)
        new.tree = memo[self.tree]
        return new


def gather_branch(node, list):
    list.append(node)
    for child in node.children:
        gather_branch(child, list)


def branch_depth(branch, current_depth):
    maximum = current_depth
    for child in branch.children:
        maximum = max(maximum, branch_depth(child, current_depth + 1))
    return maximum


def gather_branches_limited(branch, list, max_depth):
    if branch_depth(branch, 0) < max_depth:
        gather_branch(branch, list)
    else:
        for child in branch.children:
            gather_branches_limited(child, list, max_depth)


def swap_branches(tree_a, swap_a, tree_b, swap_b):
    swap_a.parent, swap_b.parent = swap_b.parent, swap_a.parent

    if tree_a.root == swap_a:
        tree_a.root = swap_b
        swap_b.update_branch_depth(0)
    else:
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

    for node in nodes_in_a:
        tree_a.nodes.remove(node)
    for node in nodes_in_b:
        tree_b.nodes.remove(node)

    tree_b.nodes.extend(nodes_in_a)
    tree_a.nodes.extend(nodes_in_b)


def crossover(a, b, max_depth):
    new_a, new_b = deepcopy(a), deepcopy(b)
    swap_a = random.choice(new_a.tree.nodes)

    valid_in_b = []
    gather_branches_limited(new_b.tree.root, valid_in_b,
                            max_depth - swap_a.depth - 1)

    swap_b = random.choice(valid_in_b)
    swap_branches(new_a.tree, swap_a, new_b.tree, swap_b)
    return new_a, new_b


def mutation(a, terminals, functions, depth, max_depth):
    new = deepcopy(a)
    swap_node = random.choice(new.tree.nodes)
    parent = swap_node.parent
    new.tree.remove(swap_node)
    parent_depth = 0 if not parent else parent.depth
    mutation_depth = min(depth, max_depth - parent_depth - 1)
    new.grow(parent, terminals, functions, mutation_depth)
    return new


def reproduction(a):
    return deepcopy(a)
