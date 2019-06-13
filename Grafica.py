import matplotlib.pyplot as plt
import numpy as np

class Grafica:

    def showPlot(self, data):

        dadesAux = data['initCamio']
        dadesAux2 = data['endCamio']
        dades = []
        for i in range(len(dadesAux)-1):
            if dadesAux[i] != "-" and dadesAux2[i] != "-":
                dades.append(dadesAux2[i]-dadesAux[i])
        plt.interactive(False)
        fig1, ax1 = plt.subplots()
        ax1.set_title('Temps estada camions en la terminal (minuts)')
        ax1.boxplot(dades)
        for i in range(len(dades)):
            y = dades[i]
            x = np.random.normal(1, 0.08, size=1)
            plt.plot(x, y, 'r.', alpha=0.2)
        plt.show()