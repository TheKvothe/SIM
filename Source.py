import numpy as np


class Source:

    num = None
    sources = []*14
    constantCamionesCadaHora = [70, 90, 140, 160, 170, 170, 150, 120, 120, 160, 170, 170, 170, 150]
    iteradorCamiones = 0
    iteradorHoras = 0
    constanteSumatorio = 0
    result = 0

    def __init__(self, data):
        self.num = data
        self.sources = [[0 for x in range(0)] for y in range(len(self.constantCamionesCadaHora))]
        for i in range(len(self.constantCamionesCadaHora)):
            for j in range(self.constantCamionesCadaHora[i]):
                if j == 0 and i != 0:
                    self.constanteSumatorio = self.sources[i-1][-1]
                self.sources[i].append(np.random.random_integers(0, 60) + self.constanteSumatorio)
            self.sources[i].sort()
            #print(self.sources[i])
            j = len(self.sources[i])-1
            while j > 0:
                if j == 0 and i != 0:
                    self.sources[i][j] -= self.sources[i-1][-1]
                else:
                    self.sources[i][j] -= self.sources[i][j-1]
                j -= 1
            #print(self.sources[i])
        #exit(0)

    def nextArrival(self):
        if self.iteradorCamiones >= len(self.sources[self.iteradorHoras]):
            self.iteradorHoras += 1
            self.iteradorCamiones = 0
        if (self.iteradorHoras >= len(self.sources)):
            self.result = -1
        else:
            self.result = self.sources[self.iteradorHoras][self.iteradorCamiones]
            self.iteradorCamiones += 1
        return self.result

    def name(self):
        return "generador"