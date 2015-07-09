from indiv import Indiv, Var

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