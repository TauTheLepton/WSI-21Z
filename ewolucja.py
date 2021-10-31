import numpy as np
import random
import math
import matplotlib.pyplot as plt
from numpy.core.numeric import identity

# params
iter_count = 1 * 10**5
init_pop_type = 2 # 0 = all the same generated randomly; 1 = each one generated individually and randomly; 2 = spaced evenly across search space
pop_size = 20 # must be even
tournament = 10 # nie ma
elite_count = 1
sigma = 0.1
mut_probab = 0.1 # nie ma
goal = 0 # ????? nie ma
alpha = 0.1
generate_start = -10
generate_end = 10

def calc_my_func(individual):
    x = individual[0]
    y = individual[1]
    return x ** 2 - 30 * x + y ** 2 - 30 * y + 450

def calc_rosenbrock_func(individual):
    x = individual[0]
    y = individual[1]
    a = 1
    b = 100
    return (a - x)**2 + b*(y - x**2)**2

def calc_bird_func(individual):
    x = individual[0]
    y = individual[1]
    return math.sin(x) * math.exp((1 - math.cos(y)) ** 2) + math.cos(y) * math.exp((1 - math.sin(x)) ** 2) + (x - y) ** 2

# penalty function
def penalty_func(delta):
    return delta * 2

# adds the penalty function
def penalize(population):
    pass

# initialization
def initialization(init_pop_type, pop_size, generate_start, generate_end):
    population = []
    # everyone is the same
    if init_pop_type == 0:
        temp = np.array([random.randrange(generate_start, generate_end), random.randrange(generate_start, generate_end)])
        for i in range(pop_size):
            population.append(temp)
    # every one is different and random
    elif init_pop_type == 1:
        for i in range(pop_size):
            population.append(np.array([random.randrange(generate_start, generate_end), random.randrange(generate_start, generate_end)]))
    # everyone is different and evenly spaced apart, except the ones that couldn't do so
    elif init_pop_type == 2:
        distance = (generate_end - generate_start) / (math.trunc(math.sqrt(pop_size)) - 1)
        last_oneI = generate_start
        for i in range(math.trunc(math.sqrt(pop_size))):
            last_oneJ = generate_start
            for j in range(math.trunc(math.sqrt(pop_size))):
                population.append(np.array([last_oneI, last_oneJ]))
                last_oneJ += distance
            last_oneI += distance
        for i in range(pop_size - math.trunc(math.sqrt(pop_size)) ** 2):
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
        parent1_idx = random.randrange(0, len(todo))
        parent2_idx = parent1_idx
        while parent2_idx == parent1_idx:
            parent2_idx = random.randrange(0, len(todo))
        child1, child2 = cross_one(population[parent1_idx], population[parent2_idx], alpha)
        population.append(child1)
        population.append(child2)
        if parent1_idx > parent2_idx:
            todo = np.delete(todo, parent1_idx)
            todo = np.delete(todo, parent2_idx)
        else:
            todo = np.delete(todo, parent2_idx)
            todo = np.delete(todo, parent1_idx)
    return population

# mutation
def mutation(population, sigma):
    population_new = []
    for individual in population:
        individual_new = np.add(individual, sigma * np.random.normal(loc = 0, scale = 1))
        population_new.append(individual_new)
    return population_new

# sort
def sort_succeed_select(population, elite_count, calc_func):
    fit = [] # vector with all fit values (?)
    for individual in population:
        fit.append(calc_func(individual))
    # sorts descending
    fit, population = zip(*sorted(zip(fit, population)))
    population = list(population)
    fit = list(fit)
    population = population[0:pop_size]
    fit = fit[0:pop_size]
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

def main():
    # evolution WHOLE
    calc_func = calc_bird_func
    population = initialization(init_pop_type, pop_size, generate_start, generate_end)
    population_history = [population]
    for i in range(iter_count):
        population = cross(population, alpha)
        population = mutation(population, sigma)
        population = sort_succeed_select(population, elite_count, calc_func)
        population_history.append(population)
        print(' ', str(math.trunc(i*100/iter_count)) + '%', end='\r')
    print('  100%')
    print(population[0])

    # plot
    plotX = []
    plotY = []
    for population in population_history:
        for individual in population:
            plotX.append(individual[0])
            plotY.append(individual[1])
    plt.plot(plotX, plotY, 'o')
    plt.show()

if __name__ == '__main__':
    main()
