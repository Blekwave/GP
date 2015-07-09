from inspect import getargspec

class Prim(object):
    def __init__(self, prim):
        if not callable(prim):
            self.prim = lambda: prim
            self.num_args = 0
        else:
            self.prim = prim
            self.num_args = len(getargspec(prim).args)

    def __call__(self, *args):
        return self.prim(*args)

    def __str__(self):
        if self.num_args == 0:
            return "Call: " + str(self.prim())
        else:
            return self.prim.__str__()
