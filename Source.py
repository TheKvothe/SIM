import numpy as np


class Source:

    num = None
    sources = [None]*5
    iterador = -1

    def __init__(self, data):
        self.num = data
        self.sources = [3, 3, 3, 3, -1]
        '''if (self.num == 1):
            self.sources = np.random.exponential(1, 4).tolist()
        elif (self.num == 2):
            print("TODO")'''

    def nextArrival(self):
        self.iterador += 1
        #print(self.sources[self.iterador])
        return self.sources[self.iterador]

    def name(self):
        return "generador"