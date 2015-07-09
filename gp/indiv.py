import random

from tree import Tree
from prim import Prim
from var import Var


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
        terminals = [Prim(prim) if not issubclass(
            type(prim), Prim) else prim for prim in terminals]
        functions = [Prim(prim) for prim in functions]
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