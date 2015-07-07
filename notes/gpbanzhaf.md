CH5 - Basic Concepts - The Foundation
=====================================

GP systems' main features
-------------------------

- Stochastic decision making
- Program structures: terminals and functions
- Genetic operators: crossover, mutation and reproduction
- Evolution by means of fitness-based selection

Primitives: Terminals and Functions
-----------------------------------

- Terminals provide values by themselves. Functions process existing values in the system. Together, terminals and functions are nodes.
- Terminals contain the inputs to the GP program, constants supplied to it (_random ephemeral constants_) and zero-argument functions with side-effects. They lie in the end of every branch in a tree-structured genome.
- __Arity__: number of arguments of a function
- In tree structure GP, constants never change their values by themselves; only through arithmetic functions.
- Functions, statements and operators compose the __function set__. There's enormous amounts of kinds of functions that may be used: arithmetic, boolean, transcendental, assignment, indexed memory, conditional statements, loops and other kinds of control and even subroutines.
- Parsimony is a virtue: not very many functions or constants are needed to get good results. GP excels in combining these in order to achieve the desired results.
- Functions must be able to handle all possible inputs. For example, regular division is not a valid GP function, because dividing by zero is not possible. The function must be modified in order to handle the exception gracefully.

Executable program structures
-----------------------------

- Primitives must be assembled into structures in order to be executed.
- Three major program structure forms: tree, linear and graph.
- Tree-structured programs: postfix (or prefix) order of evaluation, local memory.
- Linearly-structured programs: linear flow, global memory (necessary for function parameters, for example).
- Graph-structured programs (PADO): flow defined by the graph's edges, begins at start vertex and ends at end vertex. Functions operate by pushing to or popping from a localized memory stack. There's also indexed, global memory.

Population initialization
-------------------------

- Define maximum size allowed (in depth or number of nodes, for tree representations)
- Define terminal and function sets.
- Define initialization method - _grow_ vs _full_:
    - grow: randomly add nodes, stop when a terminal is added, add a terminal on max depth. Tends to create irregular trees.
    - full: add only functions until max depth, when terminals are added. Always generates regular structures.
    - ramped-half-and-half: combines both methods, choosing which one to use at each level of depth. Enhances population diversity.
- Linear initialization works differently (disregarded)

Genetic operators
-----------------

- Crossover
- Mutation
- Reproduction

### Crossover ###

A certain mating selection policy is defined, and, based on it, two individuals are selected. From these, two random subtrees are chosen and swapped. There can be bias so that subtrees containing only terminals have lower probability of being chosen. The resulting individuals are children.

### Mutation ###

After crossover, children undergo mutation with low probability. In this process, a point in the tree is chosen, and its subtree is swapped with a new, randomly generated subtree (using the methods mentioned before).

### Reproduction ###

An individual is selected and copied.

Fitness and Selection
---------------------

__Fitness function__: function calculated based on the training set, used to continuously grade individuals.

- Continuous fitness function: improvements lead to proportional improvements in the measured fitness.
- Standardized fitness: the most fit individual is assigned zero. Fitness should be minimized.
- Normalized fitness: transformed fitness function where fitness is always a value between 0 and 1.

(Note: the above are __not mutually exclusive__.)

__Selection__ is the process of deciding whether to apply genetic operators to an individual and whether to keep it in the population or not. This task is assigned to the __selection operator__.

### GA vs ES scenarios ###

- Genetic algorithms' scenario for selection involves a population with known fitness, from which individuals are selected for variation (based on their fitness) and modified. They're, then, reinserted into the next generation.
- Evolution strategy's scenario for selection is comprised of a population which is first varied, then evaluated (based on their fitness) and selected.

### Selection methods ###

- Fitness-proportional selection
- Truncation/(mi, lambda) selection
- Ranking selection
- Tournament selection

CH1 - Genetic Programming as Machine Learning
=============================================

Key parts of the machine learning process
-----------------------------------------

- Learning domain: problem or set of facts where measurable features and results to be predicted can be found.
- Training set: set where distinct instances of the relationships between features and the desired results can be found, used for training the system.
- Learning system
- Testing

Generalization capability: can the learning system make correct predictions for other input sets or has it just memorized the training set? (ic: _test set_)

ML representation types
-----------------------

- Boolean representations: conjunction and disjunction operators
- Threshold representations: threshold unit (many kinds)
- Case-based representations: store training instances as representations of classes ( outputs) or general descriptors of classes (e.g. by averaging)
  K-nearest neighbor classification method: combination of all three previous methods
- Tree representations: decision trees
- Genetic representations: can be used to represent all other forms of representation; GP representations are a superset of all other machine learning representations.

Despite the fact genetic reprs. are only limited by turing completeness and the speed of the machine used, it is often useful to constrain the used representations.

GP evolves variable-length programs. This can be very powerful.

Search operators
----------------

These define how and in which order solutions are chosen to be tested in an ML system. They transform and limit the area of the representation space to be actually searched.

- Generality/specificity operators: searches from general to specific concepts (easily viewed in boolean and threshold representations)
- Gradient descent operators: ??? (neural networks)
- GP operators: crossover (combines two individuals), mutation (changes one individual); pseudo-random.

Search strategies
-----------------

- Blind search: based on structure only (e.g., for trees, BFS and DFS). Impractical in GP due to the curse of dimensionality.
- Hill climbing: starts in an arbitrary point of the search space. Performs transformations and keeps them if the new results are better than the previous ones.
- Beam search: limits the search space by selecting a certain number of promising solutions through some evaluation metric and discarding all other solutions.
  __GP is considered a form of beam search__, because the size of the population is smaller than the set of all possible solutions. In this case, the evaluation metric used is the "__fitness function__" in GP.

Learning approaches
-------------------

- Supervised learning: the training instances contain both the input and the __correct output__. The fitness function compares the expected output with the candidate solution (usually, but many fitness functions are more complex than simply that). 
- Unsupervised learning: the training instances contain only the input. The system is supposed to look for patterns in the input data. GP is generally not used for unsupervised learning.
- Reinforcement learning: something in between supervised and unsupervised learning. Correct outputs are not specified, but the algorithm is fed back some response about the quality of the generated results, albeit not very specific.
