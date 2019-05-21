from Source import Source  # Generador
from MainGate import MainGate
from Esdeveniments import Esdeveniment
import constants


class Motor:
    """
    Motor de simulacio,
	s'encarrega de crear els primers esdeveniments
	que encadenaren la resta.
	"""

    esdevenimentsPendents = None
    esdevenimentsProcessats = None
    operadores = None
    currentTime = 0
    debugTic = 0
    kpi = None
    roundrobin = None
    maxTolerancia = 0
    replica = 0
    escenari = None
    properTancament = 0
    peticionsRebudes = 0
    primerServei = 0
    darrerServei = 0

    generador = None
    Parking = []
    MainGate = []
    cuaMainGate = 0
    cuaParking = 0
    traza = []

    def __init__(self):
        self.generador = Source(1)
        self.cuaMainGate = 0
        self.cuaParking = 0
        for i in range(0, 8):
            self.MainGate[i] = MainGate(i)
        for i in range(0, 100):
            self.Parking[i] = PosicioParking(i)
        self.esdevenimentsPendents = []
        self.esdevenimentsProcessats = []
        self.currentTime = 0

        self.inicialitzarLlistaEsdeveniments()

    def inicialitzarLlistaEsdeveniments(self):
        esd = Esdeveniment(self.generador.nextArrival(), constants.EV_ARRIVAL, self.generador)
        self.esdevenimentsPendents.append(esd)
        self.traza.append(esd.programat())

    def run(self):
        continuar = True
        while len(self.esdevenimentsPendents) and continuar:
            esdeveniment = self.esdevenimentsPendents.pop(0);
            continuar = self.tractarEsdeveniment(esdeveniment)
        for i in range(0, len(self.traza)):
            print(self.traza[i])

    def tractarEsdeveniment(self, esdeveniment):
        self.currentTime = esdeveniment.timestamp
        self.traza.append(esdeveniment.arribadaCamio())
        if esdeveniment.tipus == constants.EV_ARRIVAL_MAINGATE:
            nextTime = self.generador.nextArrival()
            if nextTime >= 0:
                nextTime += self.currentTime
                esd = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.generador)
                self.esdevenimentsPendents.append(esd)
                self.traza.append(esd.programat())
            foundMainGate = False
            for i in range(0, 8):
                if self.MainGate[i].isFree():
                    foundMainGate = True
                    foundParking = False
                    for x in range(0, 100):
                        if self.Parking[x].isFree():
                            foundParking = True
                            # nextTime-> determinar tiempo SEGUN si hay sitio o no
                            nextTime = self.currentTime
                            self.traza.append(self.MainGate[i].iniciMaingate(self.currentTime))
                            esd1 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_MAINGATE, self.MainGate[i])
                            self.esdevenimentsPendents.append(esd1)
                            self.traza.append(esd1.esperantMainGate())

                            # hay que ver como hacemos lo de la traza del parking
                            esd2 = Esdeveniment(nextTime, constants.EV_ARRIVAL_PARKING, self.Parking[x])
                            self.esdevenimentsPendents.append(esd2)
                            self.traza.append(esd2.esperantMainGate())
                            break
                    if not foundParking:
                        self.cuaParking += 1
                        self.traza.append(esdeveniment.encuar(self.cuaParking))
                    # tocar algo de la traza
                    break
            if not foundMainGate:
                self.cuaMainGate += 1
                self.traza.append(esdeveniment.encuar(self.cuaMainGate))

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_MAINGATE:
            esdeveniment.element.Free()
            if self.cua > 0:
                self.cua -= 1
                foundParking = False
                for x in range(0, 100):
                    if self.Parking[x].isFree():
                        foundParking = True  # nextTime-> determinar tiempo SEGUN si hay sitio o no
                        nextTime = self.currentTime
                        self.traza.append(esdeveniment.element.iniciMaingate(self.currentTime))
                        esd1 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_MAINGATE, esdeveniment.element)
                        self.esdevenimentsPendents.append(esd1)
                        self.traza.append(esd1.esperantMainGate())

                        # hay que ver como hacemos lo de la traza del parking
                        esd2 = Esdeveniment(nextTime, constants.EV_ARRIVAL_PARKING, self.Parking[x])
                        self.esdevenimentsPendents.append(esd2)
                        self.traza.append(esd2.esperantMainGate())
                        break
                if not foundParking:
                    self.cuaParking += 1
                    self.traza.append(esdeveniment.encuar(self.cuaParking))
                # tocar algo de la traza
        elif esdeveniment.tipus == constants.EV_ARRIVAL_PARKING:
            # cuando llega alguien al parking habra que programar el evento de final de uso del parking
            self

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_PARKING:

            # arreglar los elementos de la traza para que acepte el parking
            esdeveniment.element.Free()
            if self.cua > 0:
                self.cua -= 1
                nextTime = esdeveniment.element.nextEndService()
                nextTime += self.currentTime
                self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                esd3 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_PARKING, esdeveniment.element)
                self.esdevenimentsPendents.append(esd3)
                self.traza.append(esd3.programat())
        self.esdevenimentsPendents.sort()
