import constants

class PosicioParking:

    libre = constants.IDLE
    instancia = None
    nextTime = 10
    numGat = None

    def __init__(self, instancia):
        self.libre = True
        self.instancia = instancia

    def isFree(self):
        return self.libre == constants.IDLE

    def stateBusy(self):
        self.libre = constants.BUSY

    def Free(self):
        self.libre = constants.IDLE

    def nextEndService(self):
        self.libre = constants.BUSY
        return self.nextTime

    def iniciServei(self, temps):
        nombre = self.name()
        return "    " + nombre + " inicia Servei a " + str(temps)

    def name(self):
        return "Posicio del parking " + str(self.instancia)
