from Source import Source # Generador
from MainGate import MainGate
from Esdeveniments import Esdeveniment
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
	mainGate1= None
	mainGate2= None
	mainGate3= None
	mainGate4= None
	mainGate5= None
	mainGate6= None
	mainGate7= None
	mainGate8= None
	cua = 0
	traza = []

	def __init__(self):
		self.generador = Source(1)
		self.cua = 0
		self.mainGate1 = MainGate(0)
		self.mainGate2 = MainGate(1)
		self.mainGate3 = MainGate(2)
		self.mainGate4 = MainGate(3)
		self.mainGate5 = MainGate(4)
		self.mainGate6 = MainGate(5)
		self.mainGate7 = MainGate(6)
		self.mainGate8 = MainGate(7)
		self.esdevenimentsPendents = []
		self.esdevenimentsProcessats = []
		self.currentTime = 0

		self.inicialitzarLlistaEsdeveniments()

	def inicialitzarLlistaEsdeveniments(self):
		esd = Esdeveniment(self.generador.nextArrival(), constants.EV_ARRIVAL, self.generador)
		self.esdevenimentsPendents.append(esd)
		self.traza.append(esd.programat())
		self.cua = 0

	def run(self):
		continuar = True
		while len(self.esdevenimentsPendents) and continuar:
			esdeveniment = self.esdevenimentsPendents.pop(0);
			continuar = self.tractarEsdeveniment(esdeveniment)
		for i in range(0,len(self.traza)):
			print(self.traza[i])

	def tractarEsdeveniment(self, esdeveniment):
		self.currentTime = esdeveniment.timestamp

		self.traza.append(esdeveniment.arribadaCamio())
		if esdeveniment.tipus == constants.EV_ARRIVAL:
			nextTime = self.generador.nextArrival()
			if nextTime >= 0:
				nextTime += self.currentTime
				esd = Esdeveniment(nextTime, constants.EV_ARRIVAL, self.generador)
				self.esdevenimentsPendents.append(esd)
				self.traza.append(esd.programat())
			if self.mainGate1.isFree():
				print("jojos")

				# nextTime-> determinar tiempo SEGUN si hay sitio o no
				nextTime = self.currentTime
				self.traza.append(self.mainGate1.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate1)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())
			elif self.mainGate2.isFree():
				nextTime = self.currentTime
				self.traza.append(self.mainGate2.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate2)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())
			elif self.mainGate3.isFree():
				nextTime = self.currentTime
				self.traza.append(self.mainGate3.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate3)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())
			elif self.mainGate4.isFree():
				nextTime = self.currentTime
				self.traza.append(self.mainGate4.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate4)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())
			elif self.mainGate5.isFree():
				nextTime = self.currentTime
				self.traza.append(self.mainGate5.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate5)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())
			elif self.mainGate6.isFree():
				nextTime = self.currentTime
				self.traza.append(self.mainGate6.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate6)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())
			elif self.mainGate7.isFree():
				nextTime = self.currentTime
				self.traza.append(self.mainGate7.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate7)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())
			elif self.mainGate8.isFree():
				nextTime = self.currentTime
				self.traza.append(self.mainGate8.iniciMaingate(self.currentTime))
				esd1 = Esdeveniment(nextTime, constants.EV_ARRIVAL_MAINGATE, self.mainGate8)
				self.esdevenimentsPendents.append(esd1)
				self.traza.append(esd1.esperantMainGate())

			# elifs de 8 maingates
			else:
				self.cua += 1
				self.traza.append(esdeveniment.encuar(self.cua)) 
