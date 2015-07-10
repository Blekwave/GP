from .prim import Prim
from copy import deepcopy


class Var(Prim):

    """Variable primitive, whose value is defined before calling Indiv.eval.

    This is a special type of primitive which doesn't have a defined value out
    of the box. Instead, when evaluating an individual, its value is defined.

    When initialized, the new variable must be labeled. This is used to iden-
    tify and properly evaluate the value of a variable. Variables take a sin-
    gle parameter when called, which is the dictionary of variable values, from
    which it should find out its own."""

    def __init__(self, label):
        """Initializes a variable, defining its label."""
        self.label = label
        self.num_args = 0

    def __call__(self, variables):
        """Returns the value of the variable as defined in the dictionary.

        variables -- dictionary indexed by the variables' labels, containing
                     each variable's value."""
        return variables[self.label]

    def __str__(self):
        """String representation of the primitive (used for debugging)."""
        return "Variable " + self.label

    def __copy__(self):
        """Shallowly copies the primitive."""
        return type(self)(self.label)

    def __deepcopy__(self, memo):
        """Performs a deep copy of the primitive. Will memo hashable types."""
        if self.label not in memo:
            memo[self.label] = deepcopy(self.label, memo)
        return type(self)(memo[self.label])
