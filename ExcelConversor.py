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
        'eventTime': []
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
            'eventTime':[]
        }

    def addEsdevenimentMaingate(self, time, typeEvent, numberCamio, numberMaingate, initCamio, endCamio, eventScheduled, eventTime):
        self.traza['time'].append(time)
        self.traza['event'].append(typeEvent)
        self.traza['numberCamio'].append(numberCamio)
        self.traza['numberMainGate'].append(numberMaingate)
        self.traza['initCamio'].append(initCamio)
        self.traza['endCamio'].append(endCamio)
        self.traza['eventScheduled'].append(eventScheduled)
        self.traza['eventTime'].append(eventTime)
        #constants
        self.traza['numberParking'].append("-")
        self.traza['numberEstibador'].append("-")

    def addEsdevenimentParking(self, time, typeEvent, numberCamio, numberParking, initCamio, endCamio, eventScheduled, eventTime):
        self.traza['time'].append(time)
        self.traza['event'].append(typeEvent)
        self.traza['numberCamio'].append(numberCamio)
        self.traza['numberParking'].append(numberParking)
        self.traza['initCamio'].append(initCamio)
        self.traza['endCamio'].append(endCamio)
        self.traza['eventScheduled'].append(eventScheduled)
        self.traza['eventTime'].append(eventTime)
        # constants
        self.traza['numberMainGate'].append("-")
        self.traza['numberEstibador'].append("-")

    def addEsdevenimentEstibador(self, time, typeEvent, numberCamio, numberEstibador, initCamio, endCamio, eventScheduled, eventTime):
        self.traza['time'].append(time)
        self.traza['event'].append(typeEvent)
        self.traza['numberCamio'].append(numberCamio)
        self.traza['numberEstibador'].append(numberEstibador)
        self.traza['initCamio'].append(initCamio)
        self.traza['endCamio'].append(endCamio)
        self.traza['eventScheduled'].append(eventScheduled)
        self.traza['eventTime'].append(eventTime)
        # constants
        self.traza['numberParking'].append("-")
        self.traza['numberMainGate'].append("-")

    def export(self):
        auxExport = pand.DataFrame(self.traza, columns=['time', 'event', 'numberCamio', 'numberMainGate', 'numberParking', 'numberEstibador', 'initCamio', 'endCamio', 'eventScheduled', 'eventTime'])
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'TrazaAExcel.xls')
        print (filename)
        auxExport.to_excel(filename)
