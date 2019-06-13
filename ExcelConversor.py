import pandas as pand
import os

class ExcelConversor:
    traza = {
        'time': [],
        'event': [],
        'numberCamio': [],
        'numberMainGate': [],
        'numberParking': [],
        'numberEstibador': [],
        'initCamio': [],
        'endCamio': [],
        'eventScheduled': [],
        'eventTime': [],
        'numberEntities': []
    }

    def __init__(self):
        self.traza = {
            'time':[],
            'event':[],
            'numberCamio':[],
            'numberMainGate':[],
            'numberParking':[],
            'numberEstibador':[],
            'initCamio':[],
            'endCamio':[],
            'eventScheduled':[],
            'eventTime':[],
            'numberEntities':[]
        }

    def addEsdevenimentMaingate(self, time, typeEvent, numberCamio, numberMaingate, initCamio, endCamio, eventScheduled, eventTime):
        self.traza['time'].append(time)
        self.traza['event'].append(typeEvent)
        self.traza['numberCamio'].append(numberCamio)
        if numberMaingate == "generador":
            self.traza['numberMainGate'].append("-")
        else:
            self.traza['numberMainGate'].append(numberMaingate)
        self.traza['initCamio'].append(initCamio)
        if endCamio == 0:
            self.traza['endCamio'].append("-")
        else:
            self.traza['endCamio'].append(endCamio)
        self.traza['eventScheduled'].append(eventScheduled)
        self.traza['eventTime'].append(eventTime)
        #constants
        self.traza['numberParking'].append("-")
        self.traza['numberEstibador'].append("-")
        self.traza['numberEntities'].append("-")

    def addEsdevenimentParking(self, time, typeEvent, numberCamio, numberParking, initCamio, endCamio, eventScheduled, eventTime):
        self.traza['time'].append(time)
        self.traza['event'].append(typeEvent)
        self.traza['numberCamio'].append(numberCamio)
        self.traza['numberParking'].append(numberParking)
        self.traza['initCamio'].append(initCamio)
        if endCamio == 0:
            self.traza['endCamio'].append("-")
        else:
            self.traza['endCamio'].append(endCamio)
        self.traza['eventScheduled'].append(eventScheduled)
        self.traza['eventTime'].append(eventTime)
        # constants
        self.traza['numberMainGate'].append("-")
        self.traza['numberEstibador'].append("-")
        self.traza['numberEntities'].append("-")

    def addEsdevenimentEstibador(self, time, typeEvent, numberCamio, numberEstibador, initCamio, endCamio, eventScheduled, eventTime):
        self.traza['time'].append(time)
        self.traza['event'].append(typeEvent)
        self.traza['numberCamio'].append(numberCamio)
        self.traza['numberEstibador'].append(numberEstibador)
        self.traza['initCamio'].append(initCamio)
        if endCamio == 0:
            self.traza['endCamio'].append("-")
        else:
            self.traza['endCamio'].append(endCamio)
        self.traza['eventScheduled'].append(eventScheduled)
        self.traza['eventTime'].append(eventTime)
        # constants
        self.traza['numberParking'].append("-")
        self.traza['numberMainGate'].append("-")
        self.traza['numberEntities'].append("-")

    def addCua(self, time, nameQueue, cua, camioiD):
        self.traza['time'].append(time)
        self.traza['event'].append(nameQueue)
        self.traza['numberCamio'].append(camioiD)
        self.traza['numberEntities'].append(cua)
        # constants
        self.traza['numberEstibador'].append("-")
        self.traza['numberMainGate'].append("-")
        self.traza['numberParking'].append("-")
        self.traza['initCamio'].append("-")
        self.traza['endCamio'].append("-")
        self.traza['eventScheduled'].append("-")
        self.traza['eventTime'].append("-")

    def export(self):
        auxExport = pand.DataFrame(self.traza, columns=['time', 'event', 'numberCamio', 'numberMainGate', 'numberParking', 'numberEstibador', 'initCamio', 'endCamio', 'eventScheduled', 'eventTime', 'numberEntities'])
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'TrazaAExcel.xls')
        print (filename)
        auxExport.to_excel(filename)
