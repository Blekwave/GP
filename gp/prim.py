from inspect import getargspec
from copy import deepcopy


class Prim(object):

    """A terminal or function which belongs to an individual.

    This class should be initialized by passing a value or a callable of some
    sort. Then, calling it with the right number of parameters will either
    return the value of the primitive or call the function assigned to it.

    A function used as a primitive must be able to accept all possible inputs
    in the context of the GP algorithm."""

    def __init__(self, prim):
        """Initializes a new primitive."""
        self.prim = prim
        if not callable(prim):
            self.num_args = 0
        else:
            self.num_args = len(getargspec(prim).args)

    def __call__(self, *args):
        """Returns the value of the terminal or function call.

        This function takes a variable self.num_args amount of arguments, so as
        to match the function's parameters."""
        if callable(self.prim):
            return self.prim(*args)
        return self.prim

    def __str__(self):
        """String representation of the primitive (used for debugging)."""
        if self.num_args == 0:
            return "Call/value: " + str(self())
        else:
            return self.prim.__str__()

    def __copy__(self):
        """Shallowly copies the primitive."""
        return type(self)(self.prim)

    def __deepcopy__(self, memo):
        """Performs a deep copy of the primitive. Will memo hashable types."""
        try:
            if self.prim not in memo:
                memo[self.prim] = deepcopy(self.prim, memo)
            return type(self)(memo[self.prim])
        except TypeError:
            return type(self)(deepcopy(self.prim, memo))


def primitive_list(list):
    """Creates a list of primitives from a list of terminals and functions."""
    return [Prim(prim) if not issubclass(type(prim), Prim) else prim
            for prim in list]
