from indiv import Indiv, Var, mutation, reproduction, crossover
from tree import Tree
from copy import deepcopy
from prim import primitive_list


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    return 0 if y == 0 else x / y

terminals = primitive_list([-5, -4, -3, 0, Var("x")])
functions = primitive_list([add, sub, mul, div])


def test1():
    bob = Indiv()
    bob.grow(bob.tree.root, terminals, functions, 3)
    return bob


def test2():
    tree1 = Tree([1, 2, 3])
    tree1.add_child([4, 5, 6], tree1.root)
    tree2 = deepcopy(tree1)
    tree2.root.data[1] = 20000
    return tree1, tree2


def test3():
    a = test1()
    b = reproduction(a)
    c = mutation(b, terminals, functions, 5, 6)
    d, e = crossover(b, c, 6)

    return a, b, c, d, e
