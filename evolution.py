#evolution process
"""
Use an evolutionary strategy to find a solutions that can derive the reference (training data) from the inputs. The
first generation is randomly generated. The next generations are based on the previous generations. Due to the
evolutionary process future generations should perform better.

Chromosome/individual refers to a list of integers the represents a possible solution.
Population a list of individuals.
Generation a population at a certain moment. Each generation produces the next generation.
"""
from cgp import *
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

half_population = 20  # 0.5 * the number of chromosomes in a single generation
nr_nodes = 20  # number of nodes in the chromosomes
node_size = 3  # size of a node in the chromosome
mutation_chance = 0.10 # (0-1) chance that an element gets a random value.
max_error = 0.0001  # stop when error is smaller than this value.


population_size = 2 * half_population# + 1 # total population size, +1 for the best previous solution


def calculate_fitness(calculated, reference):
    """
    Calculate the fitness score. It compare the calculated to the desired value (reference).
    :param calculated: The calculated value.
    :param reference: The reference/desired value.
    :return: The fitness score for thes calculated and reference values.
    """
    a = calculated[0] - reference[0]
    b = a  # calculated[1] - reference[1]
    return math.sqrt(a * a + b * b)


def diversity(population):
    """
    Give the population a diversity score. Thus how diverse the chromosomes are. Is used for debugging.
    :param population: A list of chromosomes
    :return: A diversity score for the given population.
    """
    return 1


def average(fitness_list):
    """
    Calculates the average fitness score for the fitness_list.
    :param fitness_list: A list of tuples where the 2 tuple element contains the fitness score.
    :return: The average fitness score.
    """
    total = 0
    for i in range(population_size):
        total += fitness_list[i][1]
    return total / population_size


nr_features = 4


def create_base_population(size):
    """
    Create a base population of size number of chromosomes.
    :param size: Number of chromosomes that should be created.
    :return: A randomly generated population.
    """
    population = size * [None]
    for i in range(size):
        # TODO replace 50 with something not hardcoded.
        population[i] = translate(nr_features, np.random.randint(0, 99, nr_nodes * node_size))
    return population


def exec_code_and_return_x(code_object, f, x):
    k = eval(code_object)
    l = eval("1+f[0]")
    return k

import time
import pyopencl as cl


@vectorize(['float32(float32, float32)'], target='cuda')
def gpu(features)
def test_population(population, features, reference):
    """
    Calculates for each individual in the population the fitness score using the given features.
    :param population: A list if chromosomes/individuals
    :param features: The features that should be used to calculate the fitness score
    :param reference: The references values to which the outputs must be compared to.
    :return: A list of tuples. In the tuples the first item is the chromosome id in the population and the second
    element is the fitness score.
    """
    fitness_list = population_size * [None]
    start = time.time()
    for i in range(population_size):
        fitness = 0.0
        #ct = complete_translate(population[i], len(features[0]))
        #func = ct[nr_nodes - 1]
        #code_local = compile(func, '<string>', 'eval')
        for j in range(len(features)):
            x = 2
            #output2 = exec_code_and_return_x(code_local, features[j], x)
            #output = [output2, output2]
            output = cgp(features[j], population[i])
            fitness += calculate_fitness(output, reference[j])
        fitness_list[i] = (i, fitness / len(features))
    end = time.time()
    print(end - start)
    return fitness_list


def get_index():
    index = population_size
    while (index > population_size - 1):
        index = math.floor(abs(random.normalvariate(0, 0.35 * half_population)))
    return index


def create_next_generation(fitness_list, population, best_solution):
    """
    Create the next generation based on the current population and their fitness score. The next generation is
    created using crossover and mutation.
    :param fitness_list: A sorted list of tuples. A first tuple element refers to the id in the population and the
    second element is the fitness score. The list is sorted on the fitness score.
    :param population: A list of chromosomes.
    :param best_solution: The best solution. This solution is always passed to the next generation.
    :return: A new population.
    """
    crossover_selection_list = []  # create a list that can be used to determine select parents for the next generation.
    for i in range(population_size):
        # add the chromosome index (population_size - i) times to the list.
        crossover_selection_list += (population_size - i) * [fitness_list[i][0]]

    next_generation = population_size * [None]
    for i in range(half_population):
        # select parents
      #  parent_id_1 = crossover_selection_list[random.randint(0, len(crossover_selection_list) - 1)]
      #  parent_id_2 = crossover_selection_list[random.randint(0, len(crossover_selection_list) - 1)]

        parent_id_1 = get_index()
        parent_id_2 = get_index()

        parent_1 = population[fitness_list[parent_id_1][0]]
        parent_2 = population[fitness_list[parent_id_2][0]]

        # get crossover location
        cross_location = random.randint(1, nr_nodes * node_size)

        child_1 = nr_nodes * node_size * [None]
        child_2 = nr_nodes * node_size * [None]
        for j in range(nr_nodes * node_size):
            # apply crossover
            if j < cross_location:
                child_1[j] = parent_1[j]
                child_2[j] = parent_2[j]
            else:
                child_1[j] = parent_2[j]
                child_2[j] = parent_1[j]

            # apply mutation
            if random.uniform(0, 1) < mutation_chance:
                child_1[j] = translate_item(nr_features, j, random.randint(0, 99))

            if random.uniform(0, 1) < mutation_chance:
                child_2[j] = translate_item(nr_features, j, random.randint(0, 99))

        # add children to the next generation.
        next_generation[2 * i] = child_1
        next_generation[2 * i + 1] = child_2

    # add best solution to the next generation
 #   next_generation[population_size - 1] = best_solution
    return next_generation


def evolve(features, reference):
    """
    Use an evolutionary strategy to find a solutions that can derive the reference (training data) from features.
    :param features: The input data for the model.
    :param reference: The reference data.
    :return: The best found chromosome.
    """
    population = create_base_population(population_size)
    smallest_error = -1
    best_solution = population[0]  # best seen solution

    # Simulate the generations in the evolution process.
    for g in range(5000):
        # check if done
        if smallest_error != -1 and smallest_error < max_error:
            break

        fitness_list = test_population(population, features, reference)
        fitness_list.sort(key=lambda i: i[1])  # sort the tuples on the second element, thus the fitness score
        # Check if a new best solution has been found.
        if smallest_error == -1 or fitness_list[0][1] < smallest_error:
                best_solution = population[fitness_list[0][0]]  # store the best solution
                smallest_error = fitness_list[0][1]  # store the error

                # print for debugging
                print ( population[fitness_list[0][0]])
                print (smallest_error)

                # check if it can stop
                if smallest_error < max_error:
                    print("Done")
                    break

        xs.append(g)

        interval = math.floor(population_size / len(ys))

        for i in range(len(ys)):
            ys[i].append(1 / fitness_list[interval * i][1])
        tick()
        print("Generation ", g, ", smallest error: ", fitness_list[0][1], ", error median: ",
              fitness_list[half_population][1], ", diversity: ", diversity(population))

        population = create_next_generation(fitness_list, population, best_solution)
    return best_solution

xs = []
ys = []
for i in range(10):
    ys.append([])
ax = []
fig = plt.figure()
plt.interactive(False)
print(ys)
for i in range(len(ys)):
    ax.append(fig.add_subplot(111))
plt.ion()


fig.show()
fig.canvas.draw()


def tick():
  #  for i in range(len(ys)):
  #      ax[i].clear()
    for i in range(len(ys)):
        ax[i].plot(xs, ys[i])
    fig.canvas.draw()
    plt.pause(0.001)


"""
Generate test data
"""
ref = []
f = []

for x in range(5, 20, 1):
    for y in range(5, 20, 1):
        for z in range(5, 20, 1):
            for u in range(5, 20, 1):
                f += [[x, y, z, u]]
                res = 2 * x - 3 * y + 4 * z - u * x
                ref += [[res, res]]


result = evolve(f, ref)
print(cgp(f[0], result))
print(cgp(f[1], result))
print(cgp(f[2], result))
print(cgp(f[3], result))

#debug code print result
tran =  result
for n in range(nr_nodes):
    base = n * node_size
    print(n + len(f[0]), " : ", tran[base], " ",  tran[base + 1], " ",  tran[base + 2], " ")

completeTranslate = (len(f[0]) + nr_nodes) * [""]
for t in range(len(f[0])):
    completeTranslate[t] = "F" + str(t)

for n in range(nr_nodes):
    base = n * node_size
    d = n + len(f[0])
    completeTranslate[d] = "(" + completeTranslate[tran[base]] + " " + tran[base + 2] + " " + completeTranslate[tran[base + 1]] + ")"
for t in range(len(completeTranslate)):
    print(t,  " ", completeTranslate[t])
