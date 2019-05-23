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
    camio = 0

    def __init__(self, timestamp, tipus, element, camio):
        self.timestamp = timestamp
        self.tipus = tipus
        self.element = element
        self.camio = camio

    # Criteri d'ordenacio, necessari per a simular amb coherencia temporal
    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __str__(self):
        tip = ["ARRIBADA", "FISERVEI"]
        return str(self.timestamp) + " " + tip[self.tipus] + " " + self.element.name()

    def executat(self):
        tip = ["ARRIBADA", "FI SERVEI"]
        nom = self.element.name()
        txt = "" + str(self.timestamp) + " " + nom + " executa una " + tip[self.tipus]
        return txt

    def encuar(self, cua):
        tip = ["ARRIBADA", "FI SERVEI"]
        nom = self.element.name()
        txt = "		" + str(self.timestamp) + " arribada encuar una entitat " + str(cua)
        return txt

    def programat(self):
        tip = ["ARRIBADA", "FISERVEI"]
        #nom = self.element.name()
        txt = "	" + tip[self.tipus] + " pel programada per a " + str(self.timestamp)
        return txt
#--------------------------------------------------------------------------------------------------------------------------
    def arribadaCamio(self):
        tip=["Arribada al Maingate ","Fi de servei del MainGate ", "Arribada al Parking ", "Fi de servei del Parking "]
        #nom=self.element.name()
        txt = "	" + tip[self.tipus] + " del camio " + str(self.camio) + " a les " + str(self.timestamp)
        return txt

    def enviarMainGate(self, numGate):
        tip = ["ARRIBADA", "FISERVEI"]
        #nom = self.element.name()
        txt = " " + tip[self.tipus] + " pel gate " +  str(numGate) + " del camio a l'hora " +  str(self.timestamp)

    def enviarParking(self, posParking):
        tip = ["ARRIBADA", "FISERVEI"]
        #nom = self.element.name()
        txt = " " + tip[self.tipus] + " a la posicio del parking" +  str(posParking) + " del camio a l'hora " +  str(self.timestamp)

    def posicioLliureMainGate(self, numGate):
        tip = ["ARRIBADA", "FISERVEI"]
        #nom = self.element.name()
        txt = " " + tip[self.tipus] + " del gate " +  str(numGate) + " a l'hora " +  str(self.timestamp)

    def posicioLliureParking(self, posParking):
        tip = ["ARRIBADA", "FISERVEI"]
        #nom = self.element.name()
        txt = " " + tip[self.tipus] + " de la posicio del parking " +  str(posParking) + " del camio a l'hora " +  str(self.timestamp)

    def esperantMainGate(self):
        tip = ["ARRIBADA", "FISERVEI"]
        #nom = self.element.name()
        txt = " " + tip[self.tipus] + " del gate   a l'hora " +  str(self.timestamp)