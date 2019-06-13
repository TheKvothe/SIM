from Source import Source  # Generador
from MainGate import MainGate
from PosicioParking import PosicioParking
from Esdeveniments import Esdeveniment
from Estibador import Estibador
from Camio import Camio


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
    Parking = [None]
    MainGate = [None]
    Estibadors = [None]
    cuaMainGate = 0
    cuaParking = 0
    traza = []
    camio_num = 0
    cuaParkingMaingates =[]
    CPMCamions =[]
    cuaEstibadorsParking = []
    CEPCamions =[]
    CMCamions =[]
    numParking = 0
    numGates = 0
    numEstibadors = 0


    test = 0

    def __init__(self, gates, parkings, estibadors):
        self.generador = Source(1)
        self.cuaMainGate = 0
        self.cuaParking = 0
        self.numEstibadors = estibadors
        self.numParking = parkings
        self.numGates = gates
        self.Parking = [None]*self.numParking
        self.MainGate = [None]*self.numGates
        self.Estibadors = [None]*self.numEstibadors
        for i in range(0, self.numGates):
            self.MainGate[i] = MainGate(i)
        for i in range(0, self.numParking):
            self.Parking[i] = PosicioParking(i)
        for i in range(0, self.numEstibadors):
            self.Estibadors[i] = Estibador(i)

        self.esdevenimentsPendents = []
        self.esdevenimentsProcessats = []
        self.cuaParkingMaingates = []
        self.cuaEstibadorsParking = []
        self.CEPCamions = []
        self.CPMCamions = []
        self.CMCamions = []

        self.currentTime = 0

        self.inicialitzarLlistaEsdeveniments()

    def inicialitzarLlistaEsdeveniments(self):
        self.camio_num +=1
        time = self.generador.nextArrival()

        camio = Camio(constants.RECO_DESC, self.camio_num,time)
        esd = Esdeveniment(time, constants.EV_ARRIVAL_MAINGATE, self.generador, camio)

        self.esdevenimentsPendents.append(esd)
        self.traza.append(esd.programat())

    def run(self):
        continuar = True
        while len(self.esdevenimentsPendents) and continuar:
            esdeveniment = self.esdevenimentsPendents.pop(0)
            continuar = self.tractarEsdeveniment(esdeveniment)

        f = open('result.txt', 'w')
        for i in range(0, len(self.traza)):
            #print(self.traza[i],file = f) python 3!
            print >> f, self.traza[i]


    def tractarEsdeveniment(self, esdeveniment):
        self.currentTime = esdeveniment.timestamp

        self.traza.append(esdeveniment.executat())


        if esdeveniment.tipus == constants.EV_ARRIVAL_MAINGATE:
            nextTime = self.generador.nextArrival()
            if nextTime >= 0:

                nextTime += self.currentTime
                self.camio_num += 1
                camio = Camio(constants.RECO_DESC, self.camio_num, nextTime)
                esd = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.generador, camio)
                self.esdevenimentsPendents.append(esd)
                self.traza.append(esd.programat())

            foundMainGate = False
            for i in range(0, self.numGates):
                if self.MainGate[i].isFree():
                    foundMainGate = True
                    foundParking = False
                    self.traza.append(self.MainGate[i].iniciServei(self.currentTime))
                    for x in range(0, self.numParking):
                        if self.Parking[x].isFree():
                            foundParking = True
                            nextTime = self.Parking[x].nextEndService()
                            nextTime += self.currentTime

                            esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, self.MainGate[i], esdeveniment.camio)
                            self.esdevenimentsPendents.append(esd1)
                            self.traza.append(esd1.programat())

                            esd2 = Esdeveniment(self.currentTime, constants.EV_ARRIVAL_PARKING, self.Parking[x], esdeveniment.camio)
                            self.esdevenimentsPendents.append(esd2)
                            self.traza.append(esd2.programat())

                            break
                    if not foundParking:
                        self.cuaParkingMaingates.append(self.MainGate[i])
                        self.CPMCamions.append(esdeveniment.camio)
                        self.MainGate[i].stateBusy()
                        self.cuaParking += 1
                        self.traza.append(esdeveniment.encuar("Cua de parking",self.cuaParking))
                    break
            if not foundMainGate:
                self.cuaMainGate += 1
                self.CMCamions.append(esdeveniment.camio)
                self.traza.append(esdeveniment.encuar("Cua de Maingate", self.cuaMainGate))

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_MAINGATE:
            esdeveniment.element.Free()
            if self.cuaMainGate > 0:
                self.cuaMainGate -= 1
                self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                CamioEsd = self.CMCamions.pop(0)
                foundParking = False
                for x in range(0, self.numParking):
                    if self.Parking[x].isFree():

                        foundParking = True
                        nextTime = self.Parking[x].nextEndService()
                        nextTime += self.currentTime
                        esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, esdeveniment.element,CamioEsd)
                        self.esdevenimentsPendents.append(esd1)
                        self.traza.append(esd1.programat())


                        esd2 = Esdeveniment(self.currentTime, constants.EV_ARRIVAL_PARKING, self.Parking[x], CamioEsd)
                        self.esdevenimentsPendents.append(esd2)
                        self.traza.append(esd2.programat())
                        break
                if not foundParking:

                    self.cuaParkingMaingates.append(esdeveniment.element)
                    self.CPMCamions.append(CamioEsd)
                    esdeveniment.element.stateBusy()
                    esdeveniment.cambiarCamio(CamioEsd)
                    self.cuaParking += 1
                    self.traza.append(esdeveniment.encuar("Cua de parking", self.cuaParking))

        elif esdeveniment.tipus == constants.EV_ARRIVAL_PARKING:


            foundEstibador = False
            self.traza.append(esdeveniment.element.iniciServei(self.currentTime))

            for i in range (0, self.numEstibadors):
                if self.Estibadors[i].isFree():
                    foundEstibador = True
                    nextTime = self.Estibadors[i].nextEndService(esdeveniment.camio.TipusOp)
                    nextTime += self.currentTime
                    esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_PARKING, esdeveniment.element, esdeveniment.camio)
                    self.esdevenimentsPendents.append(esd2)
                    self.traza.append(esd2.programat())

                    self.traza.append(self.Estibadors[i].iniciServei(self.currentTime))
                    esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_ESTIBADOR, self.Estibadors[i], esdeveniment.camio)
                    self.esdevenimentsPendents.append(esd2)
                    self.traza.append(esd2.programat())
                    break
            if not foundEstibador:
                self.cuaEstibadorsParking.append(esdeveniment.element)
                self.CEPCamions.append(esdeveniment.camio)
                esdeveniment.element.stateBusy()

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_ESTIBADOR:

            esdeveniment.element.Free()
            if len(self.cuaEstibadorsParking) > 0:


                elemento = self.cuaEstibadorsParking.pop(0)


                CamioEsd = self.CEPCamions.pop(0)

                nextTime = esdeveniment.element.nextEndService(CamioEsd.TipusOp)
                nextTime += self.currentTime
                esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_PARKING, elemento, CamioEsd)
                self.esdevenimentsPendents.append(esd2)
                self.traza.append(esd2.programat())

                self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_ESTIBADOR, esdeveniment.element, CamioEsd)
                self.esdevenimentsPendents.append(esd2)
                self.traza.append(esd2.programat())

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_PARKING:

            esdeveniment.camio.FiTemps(self.currentTime)
            esdeveniment.element.Free()
            if self.cuaParking > 0:
                elemento = self.cuaParkingMaingates.pop(0)
                elemento.Free()
                CamioEsd = self.CPMCamions.pop(0)
                self.cuaParking -= 1

                esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, elemento, CamioEsd)
                self.esdevenimentsPendents.append(esd1)
                self.traza.append(esd1.programat())

                nextTime = esdeveniment.element.nextEndService()
                nextTime += self.currentTime

                esd3 = Esdeveniment(self.currentTime, constants.EV_ARRIVAL_PARKING, esdeveniment.element, CamioEsd)
                self.esdevenimentsPendents.append(esd3)
                self.traza.append(esd3.programat())

        self.esdevenimentsPendents.sort()
        return True


