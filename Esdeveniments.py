from Camio import Camio

class Esdeveniment:
    """
    Una classe per a ordenar els esdeveniments, amb temps cada esdeveniment tindria la seva propia rutina d'execucio
    fent el codi mes net, pero ...
    KISS
    """
    #el temps entre arribada tendra que ser la ditribucion exponencial que le pongamos a la simulacion
    tipus = 0
    timestamp = 0
    element = None
    camio = None
    excelConversor = None

    def __init__(self, timestamp, tipus, element, camio, conversor):
        self.timestamp = timestamp
        self.tipus = tipus
        self.element = element
        self.camio = camio
        self.excelConversor = conversor

    def cambiarCamio(self, camioAux):
        self.camio = camioAux

    # Criteri d'ordenacio, necessari per a simular amb coherencia temporal
    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __str__(self):
        tip = ["ARRIBADA", "FISERVEI"]
        return str(self.timestamp) + " " + tip[self.tipus] + " " + self.element.name()

    def executat(self):
        tip = ["ARRIBADA AL MAINGATE", "FISERVEI DEL MAINGATE","ARRIBADA AL PARKING", "FISERVEI DEL PARKING", "ARRIBA D'ESTIBADOR","FISERVEI ESTIBADOR"]
        nom = self.element.name()
        #print(tip[self.tipus])
        txt = "" + str(self.timestamp) + " " + nom + " executa una " + tip[self.tipus] + " Camio " + str(self.camio.iD) + "( initCamio = " + str(self.camio.DataCreacio) + " endCamio = " + str(self.camio.DataFinalitzacio) + " )"
        if self.tipus == 0 or self.tipus == 1:
            self.excelConversor.addEsdevenimentMaingate(self.timestamp, tip[self.tipus], self.camio.iD, nom, self.camio.DataCreacio, self.camio.DataFinalitzacio, "-", self.timestamp)
        elif self.tipus == 2 or self.tipus == 3:
            self.excelConversor.addEsdevenimentParking(self.timestamp, tip[self.tipus], self.camio.iD, nom, self.camio.DataCreacio, self.camio.DataFinalitzacio, "-", self.timestamp)
        else:
            self.excelConversor.addEsdevenimentEstibador(self.timestamp, tip[self.tipus], self.camio.iD, nom, self.camio.DataCreacio, self.camio.DataFinalitzacio, "-", self.timestamp)
        return txt

    def executat_gui(self):
        tip = ["ARRIBADA,MAINGATE", "FISERVEI,MAINGATE","ARRIBADA,PARKING", "FISERVEI,PARKING", "ARRIBA,ESTIBADOR","FISERVEI,ESTIBADOR"]
        nom = self.element.name()
        txt = "" + nom +","+ str(self.timestamp) + ",EXECUTAR,"+ tip[self.tipus]+""
        print(txt)
        return txt

    def encuar(self, nameQueue,cua):
        tip = ["ARRIBADA AL MAINGATE", "FISERVEI DEL MAINGATE", "ARRIBADA AL PARKING", "FISERVEI DEL PARKING",
               "ARRIBA D'ESTIBADOR", "FISERVEI ESTIBADOR"]
        nom = self.element.name()
        txt = "		" + str(self.timestamp) + " arribada encuar a "+ nameQueue+ " " + str(cua) + " entitats. Camio " + str(self.camio.iD)
        self.excelConversor.addCua(self.timestamp, nameQueue, cua, self.camio.iD)
        return txt

    def encuar_gui(self, nameQueue, cua):
        txt = nameQueue+","+str(self.timestamp)+",ENCUAR,"+str(cua)
        return txt

    def programat(self):
        tip = ["ARRIBADA AL MAINGATE", "FISERVEI DEL MAINGATE", "ARRIBADA AL PARKING", "FISERVEI DEL PARKING",
               "ARRIBA D'ESTIBADOR", "FISERVEI ESTIBADOR"]
        nom = self.element.name()
        txt = "	" + tip[self.tipus] + " programada per a les " + str(self.timestamp) + " Camio " + str(self.camio.iD)
        if self.tipus == 0 or self.tipus == 1:
            self.excelConversor.addEsdevenimentMaingate("-", tip[self.tipus], self.camio.iD, nom, self.camio.DataCreacio, self.camio.DataFinalitzacio, self.timestamp, "-")
        elif self.tipus == 2 or self.tipus == 3:
            self.excelConversor.addEsdevenimentParking("-", tip[self.tipus], self.camio.iD, nom, self.camio.DataCreacio, self.camio.DataFinalitzacio, self.timestamp, "-")
        else:
            self.excelConversor.addEsdevenimentEstibador("-", tip[self.tipus], self.camio.iD, nom, self.camio.DataCreacio, self.camio.DataFinalitzacio, self.timestamp, "-")
        return txt
