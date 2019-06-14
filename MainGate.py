import constants

class MainGate:

    libre = constants.IDLE
    instancia = None
    nextTime = 15
    numGat = None

    def __init__(self, instancia):
        self.libre = True
        self.instancia = instancia

    def iniciMaingate (self, data):
        data

    def isFree(self):
        return self.libre == constants.IDLE

    def stateBusy(self):
        self.libre = constants.BUSY

    def Free(self):
        self.libre = constants.IDLE

    def Free_gui(self, temps):
        return ""+self.name()+","+str(temps)+",FISERVEI"

    def nextEndService(self):
        self.libre = constants.BUSY
        return self.nextTime

    def iniciServei(self, temps):
        nombre = self.name()
        return "    " + nombre + " inicia Servei a " + str(temps)

    def iniciServei_gui(self, temps):
        nombre = self.name()
        return ""+nombre+","+str(temps)+",INICISERVEI"

    def name(self):
        return "Maingate " + str(self.instancia)
