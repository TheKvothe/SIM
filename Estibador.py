import constants


class Estibador:

    libre = constants.IDLE
    instancia = None
    nextTime = 10
    numGat = None
    Time = [10, 5, 26]

    def __init__(self, instancia):
        self.libre = True
        self.instancia = instancia

    def iniciPosicioParking (self, data):
        data

    def isFree(self):
        return self.libre == constants.IDLE

    def Free(self):
        self.libre = constants.IDLE

    def nextEndService(self, tipo):
        self.libre = constants.BUSY
        return self.Time[tipo]

    def iniciServei(self, temps):
        nombre = self.name()
        return "    " + nombre + " inicia Servei a " + str(temps)

    def iniciServei_gui(self, temps):
        nombre = self.name()
        return ""+nombre+","+str(temps)+",INICISERVEI"

    def name(self):
        return "Estibador " + str(self.instancia)

#########################################################
# - Que hay que hacer para el viernes					#
# - Tema triangulacion - Como la debemos aplicar ()		#
# - Tema visual ?										#
# - Testing ?											#
# - MEJORAS ESTIBADOR:									#
#   - poner los diferentes tipos de camiones: entrega,	#
#	  recogida y entrega y recogida						#
#	- poner diferente tiempo de tiempo de proceso en	#
#	vez de 10											#
#########################################################


#explicar el documento que hicimos

