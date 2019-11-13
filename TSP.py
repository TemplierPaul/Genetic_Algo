from Individual import *
import random, math
import numpy as np
import matplotlib.pyplot as plt

SIZE = 50

COORDS = []
for i in range (SIZE):
    theta = (i/SIZE)*2*math.pi
    COORDS.append((50+25*math.cos(theta), 50+25*math.sin(theta)))

COORDS = [(random.random()*100, random.random()*100) for _ in range(SIZE)]

class TSPpath(Individual):

    def empty_init(self):
        self.value = np.zeros(SIZE)

    def random_init(self):
        self.value = np.arange(SIZE)
        np.random.shuffle(self.value)

    def toBinary(self):
        self.binary = self.value

    def fromBinary(self):
        self.value = self.binary

    def reproduce(self, other, nsplit=10):
        child = TSPpath()
        child.value = []
        n = len(self.value) / nsplit
        for i in range(nsplit):
            if i%2 :
                a = self.value
            else:
                a = other.value
            count = 0
            for j in a:
                if not(j in child.value):
                    count +=1
                    child.value.append(j)
                if count == n:
                    break
        return child

    def mutate(self, rate = 0.05):
        if random.random()<= rate:
            a = random.randint(0, len(self.value)-1)
            b = random.randint(0, len(self.value)-1)
            self.value[a], self.value[b] = self.value[b], self.value[a]
            return True
        return False

    def eval(self, squared = False):
        self.score = 0
        for i in range(len(self.value)-1):
            d = (COORDS[self.value[i]][0] - COORDS[self.value[i+1]][0]) ** 2 + (COORDS[self.value[i]][1] - COORDS[self.value[i+1]][1]) ** 2
            if squared :
                self.score += d
            else:
                self.score += math.sqrt(d)
        d0 = (COORDS[self.value[0]][0] - COORDS[self.value[-1]][0]) ** 2 + (
                    COORDS[self.value[0]][1] - COORDS[self.value[-1]][1]) ** 2
        if squared:
            self.score += d0
        else:
            self.score += math.sqrt(d0)
        return self.score

    def plot(self, title=None):
        x = [COORDS[i][0] for i in self.value] + [COORDS[self.value[0]][0]]
        y = [COORDS[i][1] for i in self.value] + [COORDS[self.value[0]][1]]
        plt.plot(x, y, 'ko')
        plt.plot(x, y, 'r')
        if not(title is None): plt.title(title)
        plt.show()

def shortest(squared = False):
    tsp = TSPpath(rand=False)
    tsp.value = np.arange(SIZE)
    tsp.eval(squared = squared)
    print("\nOptimal length:", tsp.score, '\n')
    return tsp.score
