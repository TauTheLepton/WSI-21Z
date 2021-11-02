import numpy as np
import random
import math
import matplotlib.pyplot as plt

class Evolution:

    def __init__(self, init_pop_type, pop_size, elite_count, tournament_size, sigma, alpha, mut_probab, generate_start, generate_end, calc_func):
        self.init_pop_type = init_pop_type
        self.pop_size = pop_size
        self.elite_count = elite_count
        self.tournament_size = tournament_size
        self.sigma = sigma
        self.alpha = alpha
        self.mut_probab = mut_probab
        self.generate_start = generate_start
        self.generate_end = generate_end
        self.population = []
        self.population_history = []
        self.calc_func = calc_func

    # initialization of population for evolution
    def initialization(self):
        self.population = []
        # everyone is the same
        if self.init_pop_type == 0:
            temp = np.array([random.randrange(self.generate_start, self.generate_end), random.randrange(self.generate_start, self.generate_end)])
            for i in range(self.pop_size):
                self.population.append(temp)
        # every one is different and random
        elif self.init_pop_type == 1:
            for i in range(self.pop_size):
                self.population.append(np.array([random.randrange(self.generate_start, self.generate_end), random.randrange(self.generate_start, self.generate_end)]))
        # everyone is different and evenly spaced apart, except the ones that couldn't do so
        elif self.init_pop_type == 2:
            distance = (self.generate_end - self.generate_start) / (math.trunc(math.sqrt(self.pop_size)) - 1)
            last_oneI = self.generate_start
            for i in range(math.trunc(math.sqrt(self.pop_size))):
                last_oneJ = self.generate_start
                for j in range(math.trunc(math.sqrt(self.pop_size))):
                    self.population.append(np.array([last_oneI, last_oneJ]))
                    last_oneJ += distance
                last_oneI += distance
            for i in range(self.pop_size - math.trunc(math.sqrt(self.pop_size)) ** 2):
                self.population.append(np.array([random.randrange(self.generate_start, self.generate_end), random.randrange(self.generate_start, self.generate_end)]))

    # crosses one individual
    def cross_one(self, parent1, parent2):
        child1 = self.alpha * parent1 + (1 - self.alpha) * parent2
        child2 = self.alpha * parent2 + (1 - self.alpha) * parent1
        return child1, child2

    # crosses all individuals (uses self.cross_one())
    def cross(self):
        if len(self.population) % 2 == 0:
            todo = np.arange(0, len(self.population), 1)
        else:
            todo = np.arange(0, len(self.population -1), 1)
        while len(todo) > 0:
            parent1_idx = random.randrange(0, len(todo))
            parent2_idx = parent1_idx
            while parent2_idx == parent1_idx:
                parent2_idx = random.randrange(0, len(todo))
            child1, child2 = self.cross_one(self.population[todo[parent1_idx]], self.population[todo[parent2_idx]])
            self.population.append(child1)
            self.population.append(child2)
            if parent1_idx > parent2_idx:
                todo = np.delete(todo, parent1_idx)
                todo = np.delete(todo, parent2_idx)
            else:
                todo = np.delete(todo, parent2_idx)
                todo = np.delete(todo, parent1_idx)

    # mutates all individuals in population
    def mutation(self):
        # new
        population_new = []
        for individual in self.population:
            this_probab = random.choices([False, True], weights=(1 - self.mut_probab, self.mut_probab), k=1) # why does this work if this is a list of one bool???
            if this_probab:
                add = self.sigma * np.random.normal(loc = 0, scale = 1)
            else:
                add = float(0)
            individual_new = np.add(individual, add)
            population_new.append(individual_new)
        self.population = population_new

        # # old
        # population_new = []
        # for individual in self.population:
        #     # probability
        #     add = self.sigma * np.random.normal(loc = 0, scale = 1)
        #     individual_new = np.add(individual, add)
        #     population_new.append(individual_new)
        # self.population = population_new

    # sorts individuals descending according to their goal function values and returns list of these goal function values
    def sort(self):
        fit = [] # vector with all fit values (?)
        for individual in self.population:
            fit.append(self.calc_func(individual[0], individual[1]))
        # sorts descending
        fit, self.population = zip(*sorted(zip(fit, self.population)))
        self.population = list(self.population)
        fit = list(fit)
        return fit

    # sorts, does the elite succession and does the tournament selection
    def sort_succeed_select(self):
        fit = self.sort()
        self.population = self.population[0:self.pop_size]
        fit = fit[0:self.pop_size]
        # succession (decreases population)
        population_new = []
        for i in range(self.elite_count):
            population_new.append(self.population[0])
            del self.population[0]
            del fit[0]
        # selection (tournament)

        # new
        # all tournaments
        for i in range(len(self.population)):
            # one tournament
            # selection
            fighters_idx = [i]
            for j in range(self.tournament_size - 1):
                fighters_idx.append(random.randrange(0, len(self.population) - 1))
            # do the tournament itself
            best_fighter_idx = fighters_idx[0]
            for fighter_idx in fighters_idx:
                if self.calc_func(self.population[fighter_idx][0], self.population[fighter_idx][1]) > self.calc_func(self.population[best_fighter_idx][0], self.population[best_fighter_idx][1]):
                    best_fighter_idx = fighter_idx
            population_new.append(self.population[best_fighter_idx])
        self.population = population_new

        # # old
        # for i in range(len(self.population)):
        #     fighter1_idx = i
        #     fighter2_idx = random.randrange(0, len(self.population) - 1)
        #     if fit[fighter1_idx] >= fit[fighter2_idx]:
        #         population_new.append(self.population[fighter1_idx])
        #     else:
        #         population_new.append(self.population[fighter2_idx])
        # self.population = population_new

    # saves current population to historical archive
    def save(self):
        self.population_history.append(self.population)

    # plots all historical points of algirithm
    def plot(self):
        plotX = []
        plotY = []
        for population in self.population_history:
            for individual in population:
                plotX.append(individual[0])
                plotY.append(individual[1])
        plt.plot(plotX, plotY, 'o')
        plt.show()

    # prints out current best individual and his goal function value
    def show_best(self):
        fit = self.sort()
        print(self.population[0])
        print(fit[0])

    def calc_my_func(x, y):
        return x ** 2 - 30 * x + y ** 2 - 30 * y + 450

    def calc_rosenbrock_func(x, y):
        a = 1
        b = 100
        return (a - x)**2 + b*(y - x**2)**2

    def calc_bird_func(x, y):
        return math.sin(x) * math.exp((1 - math.cos(y)) ** 2) + math.cos(y) * math.exp((1 - math.sin(x)) ** 2) + (x - y) ** 2

def main():
    # params
    iter_count = 1 * 10**6
    init_pop_type = 2 # 0 = all the same generated randomly; 1 = each one generated individually and randomly; 2 = spaced evenly across search space
    pop_size = 20
    tournament_size = 3
    elite_count = 2
    sigma = 0.1
    mut_probab = 0.2
    goal = 0 # ????? nie ma
    alpha = 0.1
    generate_start = -10
    generate_end = 10

    # evolution WHOLE
    evo = Evolution(init_pop_type, pop_size, elite_count, tournament_size, sigma, alpha, mut_probab, generate_start, generate_end, Evolution.calc_bird_func)
    evo.initialization()
    for i in range(iter_count):
        evo.cross()
        evo.mutation()
        evo.sort_succeed_select()
        evo.save()
        print(' ', str(math.trunc(i*100/iter_count)) + '%', end='\r')
    print('  100%')
    evo.show_best()
    evo.plot()

if __name__ == '__main__':
    main()
