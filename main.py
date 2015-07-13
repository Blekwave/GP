from gp import GP
from gp import Var
from gp.indiv import Indiv
from gp.prim import Prim


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    return 0 if y == 0 else x / y

terminals = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, Var('x')]

functions = [add, sub, mul, div]

training_cases = [
    (0, 0),
    (0.1, 0.005),
    (0.2, 0.020),
    (0.3, 0.045),
    (0.4, 0.080),
    (0.5, 0.125),
    (0.6, 0.180),
    (0.7, 0.245),
    (0.8, 0.320),
    (0.9, 0.405)
]


def fitness(indiv, config):
    error = 0
    for case in config["training_cases"]:
        error += (indiv.eval({'x': case[0]}) - case[1])**2
    return error

config = {
    "POP_SIZE": 300,
    "NUM_GENS": 100,
    "MAX_DEPTH": 6,
    "MAX_INITIAL_DEPTH": 4,
    "MAX_MUTATION_DEPTH": 3,
    "TOURNAMENT_SIZE": 4,
    "MUTATION_PROB": 0.1,
    "training_cases": training_cases
}


def forge_perfect():
    p = Indiv()
    div_node = p.tree.add_child(Prim(div))
    mul_node = p.tree.add_child(Prim(mul), div_node)
    p.tree.add_child(Var('x'), mul_node)
    p.tree.add_child(Var('x'), mul_node)
    p.tree.add_child(Prim(2), div_node)
    return p


def print_results(result, training_cases):
    error_sum = 0
    print("Individual")
    print(result)
    for case in training_cases:
        res = result.eval({'x': case[0]})
        error = abs(res - case[1])
        error_sum += error
        print("x = {0}: y = {1} (error: {2})".format(case[0], res, error))
    print("Error sum: {0}".format(error_sum))


def main():
    gp = GP(terminals, functions, fitness, config)
    gp.init_population()
    result = gp.run()
    print_results(result, training_cases)
    return gp

if __name__ == '__main__':
    main()
