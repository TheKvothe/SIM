from Source import Source  # Generador
from MainGate import MainGate
from PosicioParking import PosicioParking
from Esdeveniments import Esdeveniment
from Estibador import Estibador
from Camio import Camio



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

    def __init__(self):
        print("Empiezan los tests")
        self.erroridle = bcolors.FAIL + "Hauria d'estar en IDLE" + bcolors.ENDC
        self.errorbusy = bcolors.FAIL + "Hauria d'estar en BUSY" + bcolors.ENDC
        self.stateTestGates()
        self.stateTestParking()
        self.stateTestEstibadors()

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

    def stateTestEstibadors(self):

        estibador = Estibador(1)

        assert estibador.libre == constants.IDLE, self.erroridle

        estibador.nextEndService(0)

        assert estibador.libre == constants.BUSY, self.errorbusy

        estibador.Free()

        assert estibador.libre == constants.IDLE, self.erroridle

        print bcolors.OKGREEN + "Test d'Estibador correctes" + bcolors.ENDC


