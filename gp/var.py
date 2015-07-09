from prim import Prim

class Var(Prim):
    def __init__(self, label):
        self.label = label
        self.num_args = 0

    def __call__(self, variables):
        return variables[self.label]
    
    def __str__(self):
        return "Variable " + self.label