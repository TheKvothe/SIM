from Source import Source  # Generador
from MainGate import MainGate
from PosicioParking import PosicioParking
from Esdeveniments import Esdeveniment
from Estibador import Estibador
from Camio import Camio
from motor import Motor

import constants


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Testing:
    erroridle = ""
    errorbusy = ""
    errorcamio3 =""
    errorcamio4 = ""
    errortamanycua1 = ""
    errortamanycua2 = ""
    def __init__(self):
        print(bcolors.OKBLUE + "Comencen els tests"+ bcolors.ENDC)
        self.erroridle = bcolors.FAIL + "Hauria d'estar en IDLE" + bcolors.ENDC
        self.errorbusy = bcolors.FAIL + "Hauria d'estar en BUSY" + bcolors.ENDC
        self.errorcamio3 = bcolors.FAIL + "El primer camio de la cua per entrar a maingate tindria que ser el 3" + bcolors.ENDC
        self.errorcamio4 = bcolors.FAIL + "El primer camio de la cua per entrar a maingate tindria que ser el 4" + bcolors.ENDC
        self.errortamanycua1 = bcolors.FAIL + "La cua hauria de ser de 1" + bcolors.ENDC
        self.errortamanycua2 = bcolors.FAIL + "La cua hauria de ser de 2" + bcolors.ENDC
        self.stateTestGates()
        self.stateTestParking()
        self.stateTestEstibadors()
        self.flowAllFree()
        self.flowTillGate()
        self.generationQueueMainGates()
        self.generationQueueParking()
        self.flowEstibadors()
        self.controlEndParking()


    #esta funcion comprueba que los estados del maingate varian correctamente en funcion de las
    #->operaciones que se le pueden aplicar durante la ejecucion
    def stateTestGates(self):

        mainGate = MainGate(1)

        assert mainGate.libre == constants.IDLE, self.erroridle

        mainGate.nextEndService()

        assert mainGate.libre == constants.BUSY, self.errorbusy

        mainGate.Free()

        assert mainGate.libre == constants.IDLE, self.erroridle

        mainGate.stateBusy()

        assert mainGate.libre == constants.BUSY, self.errorbusy

        print bcolors.OKGREEN + "Test de MainGates correctes" + bcolors.ENDC

    #esta funcion comprueba que los estados de las posiciones de parking varian correctamente en funcion de las
    #->operaciones que se le pueden aplicar durante la ejecucion
    def stateTestParking(self):

        parking = PosicioParking(1)

        assert parking.libre == constants.IDLE, self.erroridle

        parking.nextEndService()

        assert parking.libre == constants.BUSY, self.errorbusy

        parking.Free()

        assert parking.libre == constants.IDLE, self.erroridle

        parking.stateBusy()

        assert parking.libre == constants.BUSY, self.errorbusy

        print bcolors.OKGREEN + "Test de Parking correctes" + bcolors.ENDC


    #esta funcion comprueba que los estados de los estibadores varian correctamente en funcion de las
    #->operaciones que se le pueden aplicar durante la ejecucion
    def stateTestEstibadors(self):

        estibador = Estibador(1)

        assert estibador.libre == constants.IDLE, self.erroridle

        estibador.nextEndService(0)

        assert estibador.libre == constants.BUSY, self.errorbusy

        estibador.Free()

        assert estibador.libre == constants.IDLE, self.erroridle

        print bcolors.OKGREEN + "Test d'Estibador correctes" + bcolors.ENDC

    #esta funcion comprueba que cuando un camion llega si hay posicion de parking libre y de maingate
    #->va directamente a la posicion de parking
    def flowAllFree(self):
        motor = Motor(2,2,2)
        camio = Camio(constants.RECO_DESC, 1, 0)
        esd = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, MainGate(1), camio)
        motor.tractarEsdeveniment(esd)
        assert motor.Parking[0].libre == constants.BUSY, self.errorbusy

        print bcolors.OKGREEN + "El flow cuan tot esta lliure es correcte" + bcolors.ENDC


    #esta funcion comprueba que cuando un camion llega si hay posicion de parking libre y de maingate
    #->va directamente a la posicion de parking

    def flowTillGate(self):
        motor = Motor(1,1,1)

        camio1 = Camio(constants.RECO_DESC, 1, 0)
        esd1 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio1)
        motor.tractarEsdeveniment(esd1)

        camio2 = Camio(constants.RECO_DESC, 1, 0)
        esd2 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio2)
        motor.tractarEsdeveniment(esd2)

        assert motor.Parking[0].libre == constants.BUSY, self.errorbusy

        assert motor.MainGate[0].libre == constants.BUSY, self.errorbusy

        print bcolors.OKGREEN + "El flow fins al main gate cuan tots els parkings estan ocupats es correcte" + bcolors.ENDC



    def generationQueueMainGates(self):
        motor = Motor(1,1,1)

        camio1 = Camio(constants.RECO_DESC, 1, 0)
        esd1 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE,motor.MainGate[0], camio1)
        motor.tractarEsdeveniment(esd1)

        camio2 = Camio(constants.RECO_DESC, 1, 0)
        esd2 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio2)
        motor.tractarEsdeveniment(esd2)

        camio3 = Camio(constants.RECO_DESC, 1, 0)
        esd3 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio3)
        motor.tractarEsdeveniment(esd3)

        camio4 = Camio(constants.RECO_DESC, 1, 0)
        esd4 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE,motor.MainGate[0], camio4)
        motor.tractarEsdeveniment(esd4)

        assert motor.CMCamions[0] == camio3, self.errorcamio3
        assert motor.cuaMainGate == 2, self.errortamanycua2

        print bcolors.OKGREEN + "La cual del maingate funciona correctament" + bcolors.ENDC


    def generationQueueParking(self):
        motor = Motor(2,3,2)

        camio1 = Camio(constants.RECO_DESC, 1, 0)
        esd1 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio1)
        motor.tractarEsdeveniment(esd1)

        camio2 = Camio(constants.RECO_DESC, 1, 0)
        esd2 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio2)
        motor.tractarEsdeveniment(esd2)

        camio3 = Camio(constants.RECO_DESC, 1, 0)
        esd3 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio3)
        motor.tractarEsdeveniment(esd3)

        camio4 = Camio(constants.RECO_DESC, 1, 0)
        esd4 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio4)
        motor.tractarEsdeveniment(esd4)

        assert motor.CPMCamions[0] == camio4, self.errorcamio4
        assert motor.cuaParking == 1, self.errortamanycua1

        print bcolors.OKGREEN + "La cual del parking funciona correctament" + bcolors.ENDC

    def flowEstibadors(self):
        motor = Motor(1,3,2)
        camio1 = Camio(constants.RECO_DESC, 1, 0)
        esd1 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio1)
        motor.tractarEsdeveniment(esd1)

        esd2 = Esdeveniment(0, constants.EV_ARRIVAL_PARKING, motor.Parking[0], camio1)
        motor.tractarEsdeveniment(esd2)

        camio2 = Camio(constants.RECO_DESC, 1, 0)
        esd2 = Esdeveniment(0, constants.EV_ARRIVAL_PARKING, motor.MainGate[0], camio2)
        motor.tractarEsdeveniment(esd2)

        camio3 = Camio(constants.RECO_DESC, 1, 0)
        esd3 = Esdeveniment(0, constants.EV_ARRIVAL_PARKING, motor.MainGate[0], camio3)
        motor.tractarEsdeveniment(esd3)

        camio4 = Camio(constants.RECO_DESC, 1, 0)
        esd4 = Esdeveniment(0, constants.EV_ARRIVAL_PARKING, motor.MainGate[0], camio4)
        motor.tractarEsdeveniment(esd4)

        assert motor.Estibadors[0].libre == constants.BUSY, self.errorbusy
        assert motor.Estibadors[1].libre == constants.BUSY, self.erroridle

        esd2 = Esdeveniment(0, constants.EV_ENDSERVICE_ESTIBADOR, motor.Estibadors[0], camio1)
        motor.tractarEsdeveniment(esd2)

        assert motor.Estibadors[0].libre == constants.BUSY, self.errorbusy

        print bcolors.OKGREEN + "El flow dels estibadors es correcte" + bcolors.ENDC


    def controlEndParking(self):
        motor = Motor(2,2,2)

        camio1 = Camio(constants.RECO_DESC, 1, 0)
        esd1 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio1)
        motor.tractarEsdeveniment(esd1)

        camio2 = Camio(constants.RECO_DESC, 1, 0)
        esd2 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio2)
        motor.tractarEsdeveniment(esd2)

        camio3 = Camio(constants.RECO_DESC, 1, 0)
        esd3 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio3)
        motor.tractarEsdeveniment(esd3)

        camio4 = Camio(constants.RECO_DESC, 1, 0)
        esd4 = Esdeveniment(0, constants.EV_ARRIVAL_MAINGATE, motor.MainGate[0], camio4)
        motor.tractarEsdeveniment(esd4)

        assert motor.cuaParking == 2, self.errortamanycua1
        assert motor.CPMCamions[0] == camio3, self.errorcamio3

        esd4 = Esdeveniment(0, constants.EV_ENDSERVICE_PARKING, motor.Parking[0], camio4)
        motor.tractarEsdeveniment(esd4)

        assert motor.cuaParking == 1,self.errortamanycua1
        assert motor.CPMCamions[0] == camio4, self.errorcamio4

        print bcolors.OKGREEN + "Les finalitzacions del parking funcionen correctamente" + bcolors.ENDC