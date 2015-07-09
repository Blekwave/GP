from inspect import getargspec
from copy import deepcopy

class Prim(object):
    def __init__(self, prim):
        self.prim = prim
        if not callable(prim):
            self.num_args = 0
        else:
            self.num_args = len(getargspec(prim).args)

    def __call__(self, *args):
        if callable(self.prim):
            return self.prim(*args)
        return self.prim

    def __str__(self):
        if self.num_args == 0:
            return "Call/value: " + str(self())
        else:
            return self.prim.__str__()

    def __copy__(self):
        return type(self)(self.prim)

    def __deepcopy__(self, memo):
        try:
            if not self.prim in memo:
                memo[self.prim] = deepcopy(self.prim, memo)
            return type(self)(memo[self.prim])
        except TypeError:
            return type(self)(deepcopy(self.prim, memo))
