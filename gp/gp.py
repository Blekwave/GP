from .indiv import Indiv, crossover, reproduction
from .prim import primitive_list
import random


class GP(object):
    __DEFAULT_CONFIG = {
        "CROSSOVER_PROB": 0.9,  # Complementary: reproduction
        "MAX_DEPTH": 20,
        "MAX_INITIAL_DEPTH": 8,
        "MAX_MUTATION_DEPTH": 6,
        "MUTATION_PROB": 0.05,
        "NUM_GENS": 100,
        "POP_SIZE": 100,
        "TOURNAMENT_SIZE": 10,
        "MINIMIZE_FITNESS": True
    }

    def parse_config(self, config):
        """Parses config dictionary into object properties.

        config -- configuration dictionary."""
        self.crossover_prob = config["CROSSOVER_PROB"]
        self.max_depth = config["MAX_DEPTH"]
        self.max_initial_depth = config["MAX_INITIAL_DEPTH"]
        self.minimize_fitness = config["MINIMIZE_FITNESS"]
        self.max_mutation_depth = config["MAX_MUTATION_DEPTH"]
        self.mutation_prob = config["MUTATION_PROB"]
        self.num_gens = config["NUM_GENS"]
        self.pop_size = config["POP_SIZE"]
        self.tournament_size = config["TOURNAMENT_SIZE"]

    def __init__(self, terminals, functions, fitness, config={}):
        """Initializes GP system with primitives, fitness function and config.

        terminals -- list of terminals (not converted to Prim/Var yet)
        functions -- list of functions (not converted to Prim yet)
        fitness(Indiv indiv, dict config) -- fitness function:
            Function which rates the fitness of an individual. It may use data
            stored in the config dictionary. Meaning depends on the parameter
            'minimize_fitness'. If true, then the closest an individual is to
            zero, the better. Otherwise, the greatest value is considered the
            best.

            indiv -- individual to be evaluated.
            config -- config dictionary.
        config -- config dictionary."""

        self.terminals = primitive_list(terminals)
        self.functions = primitive_list(functions)
        self.fitness = fitness
        self.config = GP.__DEFAULT_CONFIG
        self.config.update(config)
        self.parse_config(self.config)
        self.population = None

    def init_population(self):
        """Initializes the population by grow. Necessary before calling run."""
        self.population = []
        self.pop_gen = 0
        for i in range(0, self.pop_size):
            new = Indiv()
            new.grow(None, self.terminals, self.functions,
                     self.max_initial_depth)
            self.population.append(new)

    def fitness_list(self, population):
        """Computes a fitness list of the population.

        It is indexed in the same way as the population list. The fitness of
        population(i) can, therefore, be accessed by fitness_list[i].

        population -- population for which the list will be generated."""
        result_list = []
        for indiv in population:
            result_list.append(self.fitness(indiv, self.config))
        return result_list

    def tournament(self, participants, fitness):
        """Returns the best individual of a group.

        participants -- list of INDEXES of each participant of the tournament
                        in self.population.
        fitness -- list generated by fitness_list(self.population)."""
        if self.minimize_fitness:
            return self.population[min(participants, key=lambda x: fitness[x])]
        else:
            return self.population[max(participants, key=lambda x: fitness[x])]

    def run(self, generations=None):
        """Runs the system for a certain number of generations.

        generations -- number of generations for which the system will run. If
                       left blank, self.num_gens is used."""
        if self.population is None:
            raise RuntimeError("Population is yet to be initialized.")

        if generations is None:
            generations = self.num_gens  # Loads default num_gens

        random.seed()  # Just precaution.

        for run_gen in range(generations):
            # Calculates fitness for all members
            fitness = self.fitness_list(self.population)
            best_individual = self.tournament(range(self.pop_size), fitness)
            next_generation = [best_individual]  # Elitism
            while len(next_generation) < self.pop_size:
                operator = random.random()  # Randomly defines operator

                if operator < self.crossover_prob:  # Crossover
                    participants = random.sample(range(self.pop_size),
                                                 self.tournament_size * 2)
                    a = self.tournament(participants[:self.tournament_size],
                                        fitness)
                    b = self.tournament(participants[self.tournament_size:],
                                        fitness)
                    new = crossover(a, b, self.max_depth)  # Returns tuple
                else:  # Reproduction
                    participants = random.sample(range(self.pop_size),
                                                 self.tournament_size)
                    a = self.tournament(participants, fitness)
                    new = [reproduction(a)]

                for indiv in new:
                    if len(next_generation) < self.pop_size:
                        mutate = random.random()
                        if mutate < self.mutation_prob:
                            indiv.mutate(self.terminals, self.functions,
                                         self.max_mutation_depth,
                                         self.max_depth)
                        next_generation.append(indiv)
                    else:
                        break

            self.population = next_generation
            self.pop_gen += 1

        fitness = self.fitness_list(self.population)
        best_individual = self.tournament(range(self.pop_size), fitness)
        return best_individual
