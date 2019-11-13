import random

class Individual:

    def __init__(self, rand=False):
        if rand:
            self.random_init()
        else :
            self.empty_init()
        self.score = None
        self.binary = None
        self.ID = "#" + str(random.randint(0, 10000))

    def __str__(self):
        return self.ID + ' ' + str(self.value)

    def __repr__(self):
        return '\n' + self.ID + ' ' + str(self.value) + ' -> ' + str(self.score)

    def __mul__(self, other):
        return self.reproduce(other)

    def random_init(self):
        self.value = None

    def empty_init(self):
        self.value = None

    def toBinary(self):
        self.binary = self.value
        return self.binary

    def fromBinary(self):
        self.value = self.binary
        return self.value

    def reproduce(self, other):
        child = Individual()
        return child

    def eval(self):
        return 0

