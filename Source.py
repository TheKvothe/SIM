import numpy as np

class Source:

    num = None
    sources = None

    def __init__(self, data):
        self.num = data
        if (self.num == 1):
            self.sources = np.random.exponential(1, 4).tolist()
        elif (self.num == 2):
            print("TODO")

    def nextArrival(self):
        result = self.sources[-1]
        self.sources.pop()
        return result