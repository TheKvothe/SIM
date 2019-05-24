from Source import Source  # Generador
from MainGate import MainGate
from PosicioParking import PosicioParking
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
    Parking = [None]*2
    MainGate = [None]*3
    cuaMainGate = 0
    cuaParking = 0
    traza = []
    camio_num = 0

    test = 0

    def __init__(self):
        self.generador = Source(1)
        self.cuaMainGate = 0
        self.cuaParking = 0
        self.camio_num += 1
        for i in range(0, 3):
            #print("inicializacion de los maingates" + str(i))
            self.MainGate[i] = MainGate(i)
        for i in range(0, 2):
            self.Parking[i] = PosicioParking(i)
        self.esdevenimentsPendents = []
        self.esdevenimentsProcessats = []
        self.currentTime = 0

        self.inicialitzarLlistaEsdeveniments()

    def inicialitzarLlistaEsdeveniments(self):
        esd = Esdeveniment(self.generador.nextArrival(), constants.EV_ARRIVAL_MAINGATE, self.generador, self.generador, self.camio_num)
        self.camio_num += 1
        self.esdevenimentsPendents.append(esd)
        self.traza.append(esd.programat())

    def run(self):
        continuar = True
        while len(self.esdevenimentsPendents) and continuar:
            esdeveniment = self.esdevenimentsPendents.pop(0)
            continuar = self.tractarEsdeveniment(esdeveniment)
        for i in range(0, len(self.traza)):
            print(self.traza[i])


    def tractarEsdeveniment(self, esdeveniment):
        self.currentTime = esdeveniment.timestamp

        self.traza.append(esdeveniment.executat())

        if esdeveniment.tipus == constants.EV_ARRIVAL_MAINGATE:
            nextTime = self.generador.nextArrival()
            if nextTime >= 0:
                nextTime += self.currentTime
                esd = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.generador, self.generador, self.camio_num)
                self.camio_num += 1
                self.esdevenimentsPendents.append(esd)
                self.traza.append(esd.programat())

            foundMainGate = False
            for i in range(0, 3):#ara mismo esta puesto aqui un 3 pero tendrian que ser 8
                if self.MainGate[i].isFree():
                    foundMainGate = True
                    foundParking = False
                    self.traza.append(self.MainGate[i].iniciServei(self.currentTime))
                    for x in range(0, 2):#ara mismo esta puesto aqui un 3 pero tendrian que ser 100
                        if self.Parking[x].isFree():
                            foundParking = True
                            nextTime = self.Parking[x].nextEndService()
                            nextTime += self.currentTime
                            #self.traza.append(self.MainGate[i].iniciMaingate(self.currentTime))
                            esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, self.MainGate[i], self.MainGate[i], self.camio_num)
                            self.esdevenimentsPendents.append(esd1)
                            self.traza.append(esd1.programat())

                            # hay que ver como hacemos lo de la traza del parking
                            self.traza.append(self.Parking[x].iniciServei(self.currentTime))
                            esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_PARKING, self.Parking[x], self.MainGate[i], self.camio_num)
                            self.esdevenimentsPendents.append(esd2)
                            self.traza.append(esd2.programat())
                            break
                    if not foundParking:
                        self.cuaParking += 1
                        self.traza.append(esdeveniment.encuar("Cua de parking",self.cuaParking))
                    # tocar algo de la traza
                    break
            if not foundMainGate:
                self.cuaMainGate += 1
                self.traza.append(esdeveniment.encuar("Cua de Maingate", self.cuaMainGate))

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_MAINGATE:
            esdeveniment.element.Free()
            if self.cuaMainGate > 0:
                self.cuaMainGate -= 1
                self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                foundParking = False
                for x in range(0, 2):
                    if self.Parking[x].isFree():
                        foundParking = True
                        nextTime = self.Parking[x].nextEndService()
                        nextTime += self.currentTime
                        #self.traza.append(self.MainGate[i].iniciMaingate(self.currentTime))
                        esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, esdeveniment.element, esdeveniment.element, self.camio_num)
                        self.esdevenimentsPendents.append(esd1)
                        self.traza.append(esd1.programat())

                        # hay que ver como hacemos lo de la traza del parking
                        self.traza.append(self.Parking[x].iniciServei(self.currentTime))
                        esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_PARKING, self.Parking[x], esdeveniment.element, self.camio_num)
                        self.esdevenimentsPendents.append(esd2)
                        self.traza.append(esd2.programat())
                        break
                if not foundParking:
                    self.cuaParking += 1
                    self.traza.append(esdeveniment.encuar("Cua de parking", self.cuaParking))

        elif esdeveniment.tipus == constants.EV_ARRIVAL_PARKING:
            # cuando llega alguien al parking habra que programar el evento de final de uso del parking
            self

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_PARKING:
            #falta por arreglar que saque por pantalla qual maingate se queda libre
            esdeveniment.element2.Free()
            esdeveniment.element.Free()
            if self.cuaParking > 0:
                self.cuaParking -= 1
                esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, esdeveniment.element2,esdeveniment.element2, self.camio_num)
                self.esdevenimentsPendents.append(esd1)
                self.traza.append(esd1.programat())

                nextTime = esdeveniment.element.nextEndService()
                nextTime += self.currentTime
                self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                esd3 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_PARKING, esdeveniment.element, esdeveniment.element, self.camio_num)
                self.esdevenimentsPendents.append(esd3)
                self.traza.append(esd3.programat())

        self.esdevenimentsPendents.sort()
        return True

