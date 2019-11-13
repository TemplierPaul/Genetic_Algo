from Individual import *
from TSP import TSPpath, shortest
import numpy as np
import random
import time
import matplotlib.pyplot as plt

class GenAlg():

    def __init__(self, indiv_type, pop_size=None, gen_size=None):
        assert indiv_type.toBinary
        self.indiv_type = indiv_type
        self.pop_size = pop_size
        self.gen_size = gen_size
        self.pop = None
        self.gen = 0

    def __str__(self):
        scores = [x.score for x in self.pop]
        return "GenAlg: " + str(self.pop_size) + " elts at gen " + str(self.gen) + " / " + str(self.gen_size) + "- Best : " + str(max(scores))

    def generatePopulation(self):
        self.pop = [self.indiv_type(rand=True) for _ in range(self.pop_size)]

    def reproduction(self, mut=0.05):
        true_mut = 0
        for _ in range(self.pop_size):
            a = random.randint(0, self.pop_size-1)
            b = random.randint(0, self.pop_size-1)
            #print(a, b, '/', self.pop_size)
            child = self.pop[a].reproduce(self.pop[b])
            if child.mutate(rate = mut) : true_mut += 1
            self.pop.append(child)
        return true_mut / self.pop_size

    def evaluation(self, squared = False, force=False):
        for x in self.pop:
            if x.score is None or force:
                x.eval(squared = squared)

    def selection(self):
        self.pop = list(self.pop)
        self.pop.sort(key=lambda x: x.score, reverse=False)
        self.pop = self.pop[:int(self.pop_size)]
        self.pop_size = len(self.pop)


    def run(self, max_iter_same = 20, optimal=None, mutation_rate=0.3, mutation_decrease=False, eval_squared = False):
        t = time.time()
        self.gen = 0
        last = []
        best = []
        if self.pop is None : self.generatePopulation()
        self.evaluation(squared = eval_squared)
        self.pop[0].plot('Initial random Individual')
        mut = mutation_rate
        for _ in range(self.gen_size):
            if mutation_decrease:
                mut = mut - (mutation_rate - 0.05)/self.gen_size
            self.gen +=1
            print(self)
            true_mut = self.reproduction(mut)
            print("Mutation rate:", true_mut)
            self.evaluation(squared=eval_squared)
            self.selection()
            m = max([x.score for x in self.pop])
            last.append(m)
            best.append(m)
            if len(last) >= max_iter_same:
                if max(last) - min(last) < 1:
                    break
                else :
                    last.pop(0)
        self.pop.sort(key=lambda x: x.score, reverse=False)
        self.pop[0].plot("Final best solution")
        print('\nFinal:', self.pop[0])
        print('Best score:', self.pop[0].score)
        if not (best is None):
            print("Optimal length:", optimal)
            print("Efficiency:", int(100 * optimal / last[0]), "%")
        print('\nTotal time:', time.time()-t, 's')
        plt.plot(best)
        plt.xlabel("Generations")
        if eval_squared : plt.ylabel("Squared Sum of distances")
        else: plt.ylabel("Sum of distances")
        plt.show()
        return last[0]

g = GenAlg(TSPpath, 10000, 10000)
square = True
#s = shortest(squared = square)
b = g.run(max_iter_same=50, optimal=None, mutation_rate=0.3, mutation_decrease=True, eval_squared=square)

print("Length:", g.pop[0].eval(squared=False))

g = GenAlg(TSPpath, 10000, 10000)
square = False
#s = shortest(squared = square)
b = g.run(max_iter_same=50, optimal=None, mutation_rate=0.3, mutation_decrease=True, eval_squared=square)
