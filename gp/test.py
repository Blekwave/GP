from indiv import Indiv, Var
from tree import Tree
from copy import deepcopy

def add(x,y):
    return x + y

def sub(x,y):
    return x - y

def mul(x,y):
    return x * y

def div(x,y):
    return 0 if y == 0 else x / y

def test1():
    terminals = [-5, -4, -3, 0, Var("x")]
    functions = [add, sub, mul, div]
    bob = Indiv()
    bob.grow(bob.tree.root, terminals, functions, 3)
    return bob

def test2():
    tree1 = Tree([1,2,3])
    tree1.add_child([4,5,6], tree1.root)
    tree2 = deepcopy(tree1)
    tree2.root.data[1] = 20000
    return tree1, tree2
