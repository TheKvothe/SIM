import constants


class Camio:

    TipusOp = 0
    iD = None
    DataCreacio = None
    DataFinalitzacio = None #cuando haya un fiservei parking en ese momento al camion habra que ponerle el tiempo
    #falta asssignar el fitemps

    def __init__(self, TipusOp, iD, DataCreacio):
        self.TipusOp = TipusOp
        self.iD = iD
        self.DataCreacio = DataCreacio
        self.DataFinalitzacio = 0

    def FiTemps(self, data):
        self.DataFinalitzacio = data
