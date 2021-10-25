import numpy as np
import random
# from scipy import stats

# params
iter_count = 10
pop_type_same = False # True = all the same, False = each one generated individually and randomly
pop_size = 10 # must be even
tournament = 10 # nie ma
elite_count = 1
sigma = 0.1
mut_probab = 0.1 # nie ma
goal = 0 # ????? nie ma
alpha = 0.1
generate_start = 1
generate_end = 10

def calc_func(individual):
    x = individual[0]
    y = individual[1]
    return 3 * x ** 2 + 7 * y

# initialization
def initialization(pop_type_same, pop_size, generate_start, generate_end):
    population = []
    if pop_type_same:
        temp = np.array([random.randrange(generate_start, generate_end), random.randrange(generate_start, generate_end)])
        for i in range(pop_size):
            population.append(temp)
    else:
        for i in range(pop_size):
            population.append(np.array([random.randrange(generate_start, generate_end), random.randrange(generate_start, generate_end)]))
    return population

# cross one
def cross_one(parent1, parent2, alpha):
    child1 = alpha * parent1 + (1 - alpha) * parent2
    child2 = alpha * parent2 + (1 - alpha) * parent1
    return child1, child2

# cross
def cross(population, alpha):
    todo = np.arange(0, pop_size, 1)
    # for i in range(len(population)):
    #     pass
    while len(todo) > 0:
        parent1_idx = random.randrange(0, len(todo) - 1)
        parent2_idx = parent1_idx
        while parent2_idx == parent1_idx:
            parent2_idx = random.randrange(0, len(todo) - 1)
        child1, child2 = cross_one(population[parent1_idx], population[parent2_idx], alpha)
        population.append(child1)
        population.append(child2)
        todo = np.delete(todo, parent1_idx)
        todo = np.delete(todo, parent2_idx)
    return population

# mutation
def mutation(population, sigma):
    population_new = []
    for individual in population:
        individual_new = np.add(individual, sigma * np.random.normal(loc = 0, scale = 1))
        population_new.append(individual_new)
    return population_new

# sort
def sort_succeed_select(population, elite_count):
    fit = [] # vector with all fit values (?)
    for individual in population:
        fit.append(calc_func(individual))
    # sorts descending
    fit, population = zip(*sorted(zip(fit, population)))
    # succession (decreases population)
    population_new = []
    for i in range(elite_count):
        population_new.append(population[0])
        del population[0]
        del fit[0]
    # selection (tournament)
    todo = np.arange(0, len(population), 1)
    for i in range(len(population)):
        fighter1_idx = i
        fighter2_idx = random.randrange(0, len(population) - 1)
        if fit[fighter1_idx] >= fit[fighter2_idx]:
            population_new.append(population[fighter1_idx])
        else:
            population_new.append(population[fighter2_idx])
    return population_new

# evolution WHOLE
population = initialization(pop_type_same, pop_size, generate_start, generate_end)
population_history = [population]
for i in range(iter_count):
    population = cross(population, alpha)
    population = mutation(population, sigma)
    population = sort_succeed_select(population, elite_count)
    population_history.append(population)


# population = initialization(pop_type_same, pop_size, generate_start, generate_end)
# print(population)
# population = mutation(population, sigma)
# print(population)
# population, fit = sort(population)
