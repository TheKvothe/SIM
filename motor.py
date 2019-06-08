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
    Parking = [None]*2
    MainGate = [None]*2
    Estibadors = [None]*2
    cuaMainGate = 0
    cuaParking = 0
    traza = []
    camio_num = 0
    cuaParkingMaingates =[]
    CPMCamions =[]
    cuaEstibadorsParking = []
    CEPCamions =[]
    CMCamions =[]


    test = 0

    def __init__(self):
        self.generador = Source(1)
        self.cuaMainGate = 0
        self.cuaParking = 0
        for i in range(0, 2):
            #print("inicializacion de los maingates" + str(i))
            self.MainGate[i] = MainGate(i)
        for i in range(0, 2):
            self.Parking[i] = PosicioParking(i)
        for i in range(0, 2):
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
        continuar = True
        while len(self.esdevenimentsPendents) and continuar:
            esdeveniment = self.esdevenimentsPendents.pop(0)
            continuar = self.tractarEsdeveniment(esdeveniment)
        for i in range(0, len(self.traza)):
            print(self.traza[i])


    def tractarEsdeveniment(self, esdeveniment):
        self.currentTime = esdeveniment.timestamp

        self.traza.append(esdeveniment.executat())
       # print(str(esdeveniment.element.name())+" " + self.Parking[1].name() + " esta " + str(self.Parking[1].libre))

        if esdeveniment.tipus == constants.EV_ARRIVAL_MAINGATE:
            nextTime = self.generador.nextArrival()
            #print(nextTime)
            #print(self.camio_num)
            if nextTime >= 0:

                nextTime += self.currentTime
                self.camio_num += 1
                camio = Camio(constants.DESCARREGA, self.camio_num, nextTime)
                esd = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.generador, camio)
                 # esto no se hace bien porque entra
                self.esdevenimentsPendents.append(esd)
                self.traza.append(esd.programat())

            foundMainGate = False
            for i in range(0, 2):#ara mismo esta puesto aqui un 3 pero tendrian que ser  8
                if self.MainGate[i].isFree():
                    foundMainGate = True
                    foundParking = False
                    for x in range(0, 2):
                        print("arrival maingate " + self.Parking[x].name() + " " + str(self.Parking[x].libre) + " " + str(
                            self.currentTime))
                    # print("estoy en el arrival maingate 1 , el nombre del gate es " + self.MainGate[i].name())
                    self.traza.append(self.MainGate[i].iniciServei(self.currentTime))
                    for x in range(0, 2):#ara mismo esta puesto aqui un 3 pero tendrian que ser 100
                        #print(" arrival maingate " +self.Parking[x].name() + " esta " + str(self.Parking[x].libre))
                        if self.Parking[x].isFree():
                            foundParking = True
                            nextTime = self.Parking[x].nextEndService()
                            nextTime += self.currentTime
                            #self.traza.append(self.MainGate[i].iniciMaingate(self.currentTime))
                            esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, self.MainGate[i], esdeveniment.camio)
                            self.esdevenimentsPendents.append(esd1)
                            self.traza.append(esd1.programat())

                           # print("estoy en el arrival maingate 2 , el nombre del gate es " + self.MainGate[i].name())

                            # esto no funciona porque solo te dice el maingate del qual ha entrado no el que esta esperando TONTO

                            # hay que ver como hacemos lo de la traza del parking
                            #self.traza.append(self.Parking[x].iniciServei(self.currentTime))
                            esd2 = Esdeveniment(self.currentTime, constants.EV_ARRIVAL_PARKING, self.Parking[x], esdeveniment.camio)
                            self.esdevenimentsPendents.append(esd2)
                            self.traza.append(esd2.programat())
                            #print("he dejado la " + self.Parking[x].name() + " " + str(self.Parking[x].libre)+ " soy el camion " + str(esdeveniment.camio.iD))
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
            for x in range(0, 2):
                print("end maingate "+self.Parking[x].name() + " " + str(self.Parking[x].libre)+ " " + str(self.currentTime))
           # print("estoy en el endservice del maingate, el nombre del elemento es " + esdeveniment.element.name())
            if self.cuaMainGate > 0:
                self.cuaMainGate -= 1
                self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                CamioEsd = self.CMCamions.pop(0)
                foundParking = False
                for x in range(0, 2):
                    print("he llegado aqui " + str(CamioEsd.iD))
                    #print(" end maingate " + self.Parking[x].name() + " esta " + str(self.Parking[x].libre))
                    if self.Parking[x].isFree():
                        #print("soy el camion: " + str(CamioEsd.iD) + " y la " + self.Parking[1].name() + " esta libre")
                        foundParking = True
                        nextTime = self.Parking[x].nextEndService()
                        nextTime += self.currentTime
                        #self.traza.append(self.MainGate[i].iniciMaingate(self.currentTime))#lo que esta fallabndo esque cuando entra el camion ccuatro el 3 aun no esta dentro del de parkin por lo que detecta sitio de parking libree
                        esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, esdeveniment.element,CamioEsd)
                        self.esdevenimentsPendents.append(esd1)
                        self.traza.append(esd1.programat())

                        # hay que ver como hacemos lo de la traza del parking
                        #la posicion del parking 1 no esta funcionando
                        #self.traza.append(self.Parking[x].iniciServei(self.currentTime))#esto va a volar con los estibadores
                        esd2 = Esdeveniment(self.currentTime, constants.EV_ARRIVAL_PARKING, self.Parking[x], CamioEsd)#esto tendra que ser un arrival
                        self.esdevenimentsPendents.append(esd2)
                        self.traza.append(esd2.programat())
                        break
                if not foundParking:
                    print("jajas y " + str(CamioEsd.iD))
                    self.cuaParkingMaingates.append(esdeveniment.element)
                    self.CPMCamions.append(CamioEsd)
                    esdeveniment.element.stateBusy()
                    esdeveniment.cambiarCamio(CamioEsd)
                    self.cuaParking += 1
                    self.traza.append(esdeveniment.encuar("Cua de parking", self.cuaParking))#esto creo que esta mal, falta que en la cola me saque bien que camion

        elif esdeveniment.tipus == constants.EV_ARRIVAL_PARKING:
            # cuando llega alguien al parking habra que programar el evento de final de uso del parking
            for x in range(0, 2):
                print("arrival parking  "+self.Parking[x].name() + " " + str(self.Parking[x].libre)+ " " + str(self.currentTime))

            foundEstibador = False
            self.traza.append(esdeveniment.element.iniciServei(self.currentTime))  # dentro o fuera del loop?
         #   print(esdeveniment.element.name() + " " + str(esdeveniment.element.libre) + " en el " + str(esdeveniment.timestamp))
            for i in range (0, 2):
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

            for x in range(0, 2):
                print("end estibador 1 "+self.Parking[x].name() + " " + str(self.Parking[x].libre)+ " " + str(self.currentTime))
            esdeveniment.element.Free()
            if len(self.cuaEstibadorsParking) > 0:

                #aqui esta el fallo!!!!!!!! del dia 2 de junio domingo
                elemento = self.cuaEstibadorsParking.pop(0)
                #print(elemento.libre)
                #elemento.Free()

                CamioEsd = self.CEPCamions.pop(0)

                nextTime = esdeveniment.element.nextEndService()
                nextTime += self.currentTime
                esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_PARKING, elemento, CamioEsd)
                self.esdevenimentsPendents.append(esd2)
                self.traza.append(esd2.programat())

                self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                esd2 = Esdeveniment(nextTime, constants.EV_ENDSERVICE_ESTIBADOR, esdeveniment.element, CamioEsd)
                self.esdevenimentsPendents.append(esd2)
                self.traza.append(esd2.programat())

                for x in range(0, 2):
                    print("end estibador 2 " + self.Parking[x].name() + " " + str(self.Parking[x].libre) + " " + str(
                        self.currentTime))

        elif esdeveniment.tipus == constants.EV_ENDSERVICE_PARKING:

            for x in range(0, 2):
                print("end parking "+self.Parking[x].name() + " " + str(self.Parking[x].libre)+ " " + str(self.currentTime))
            esdeveniment.camio.FiTemps(self.currentTime)
            esdeveniment.element.Free()
            if self.cuaParking > 0:
                elemento = self.cuaParkingMaingates.pop(0)
                elemento.Free()
                CamioEsd = self.CPMCamions.pop(0)
                self.cuaParking -= 1
                #envez de guardar elementos tendria que guardar esdeveniments
                #print("estoy en el endservice del parking, el nombre del elemento2 es " + esdeveniment.element2.name())
                esd1 = Esdeveniment(self.currentTime, constants.EV_ENDSERVICE_MAINGATE, elemento, CamioEsd)
                self.esdevenimentsPendents.append(esd1)
                self.traza.append(esd1.programat())

                nextTime = esdeveniment.element.nextEndService()
                nextTime += self.currentTime
                #self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
                esd3 = Esdeveniment(self.currentTime, constants.EV_ARRIVAL_PARKING, esdeveniment.element, CamioEsd)
                self.esdevenimentsPendents.append(esd3)
                self.traza.append(esd3.programat())

        self.esdevenimentsPendents.sort()
        return True
