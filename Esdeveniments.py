#ASD
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

    def __init__(self, timestamp, tipus, element):
        self.timestamp = timestamp
        self.tipus = tipus
        self.element = element

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
        nom = self.element.name()
        txt = "	" + tip[self.tipus] + " pel " + nom + " programada per a " + str(self.timestamp)
        return txt
#--------------------------------------------------------------------------------------------------------------------------
    def arribadaCamio(self):
		tip=["ARRIBADA","FISERVEI"]
		nom=self.element.name()
		txt="	"+tip[self.tipus]+" del  "+nom+" a les "+str(self.timestamp)
		return txt

    def enviarMainGate(self, numGate):
        tip = ["ARRIBADA", "FISERVEI"]
        nom = self.element.name()
        txt = " " + tip[self.tipus] + " pel gate " +  str(numGate) + " del camio a l'hora " +  str(self.timestamp)

    def enviarParking(self, posParking):
        tip = ["ARRIBADA", "FISERVEI"]
        nom = self.element.name()
        txt = " " + tip[self.tipus] + " a la posicio del parking" +  str(posParking) + " del camio " + nom + "a l'hora " +  str(self.timestamp)

    def posicioLliureMainGate(self, numGate):
        tip = ["ARRIBADA", "FISERVEI"]
        nom = self.element.name()
        txt = " " + tip[self.tipus] + " del gate " +  str(numGate) + " a l'hora " +  str(self.timestamp)

    def posicioLliureParking(self, posParking):
        tip = ["ARRIBADA", "FISERVEI"]
        nom = self.element.name()
        txt = " " + tip[self.tipus] + " de la posicio del parking " +  str(posParking) + " del camio a l'hora " +  str(self.timestamp)

    def esperantMainGater(self):
        
