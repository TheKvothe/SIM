import tkinter
import random
from time import sleep
# todo -> QUE ES PAUSI DE VERITAT
# todo -> QUE FAST i SLOW


class Canvas(tkinter.Tk):
    def __init__(self, to, delay):
        self.canvas = tkinter.Canvas(to, width=1000, height=450, relief="raised", borderwidth=1)
        self.canvas.pack(side='left')

        self.isPaused = True
        self.traza = []
        self.traza_who = []
        self.traza_time = []
        self.traza_what = []
        self.traza_oper = []
        self.traza_where = []

        self.delaySpeed = delay
        self.iterator = 0
        self.current_time = -1
        self.cua = 0

        self.rows_pkg = 4
        self.cols_pkg = 25
        self.rows_maingate = 8
        self.cols_maingate = 1
        self.rows_est = 4
        self.cols_est = 25

        self.cell_width = 20
        self.cell_height = 40
        self.cell_width_maingate = 60
        self.cell_height_maingate = 40
        self.cell_width_est = 20
        self.cell_height_est = 40
        self.generador_width = 80
        self.generador_height = 80

        self.init_x = 450
        self.init_y = 20
        self.init_x_maingate = 200
        self.init_y_maingate = 100
        self.init_x_est = 450
        self.init_y_est = 250

        self.xini = 20
        self.yini = 340
        self.xfi = self.xini + self.generador_width
        self.yfi = self.yini + self.generador_height
        self.canvas.create_text(55, 330, text="GENERADOR")
        self.generador = self.canvas.create_rectangle(self.xini, self.yini, self.xfi, self.yfi, fill="cyan",
                                                      tags="rect")

        self.xini_queue = 50
        self.yini_queue = 220
        self.xfi_queue = self.xini_queue + 100
        self.yfi_queue = self.yini_queue + 40

        self.setTerminal()

    def setTerminal(self):
        self.cua = 0
        self.canvas.create_rectangle(self.xini_queue, self.yini_queue, self.xfi_queue, self.yfi_queue, fill="white")

        self.canvas.create_text(self.xini_queue + 50, self.yini_queue - 10, text="CUA MAINGATE")
        self.queue = self.canvas.create_text(self.xini_queue + 50, self.yini_queue + 20, text=self.cua, font="Times 20")
        self.canvas.create_text(self.init_x_maingate + 30, self.init_y_maingate - 10, text="MAINGATE")

        self.maingate = {}
        for col in range(self.cols_maingate):
            for row in range(self.rows_maingate):
                x1 = self.init_x_maingate + col * self.cell_width_maingate
                y1 = self.init_y_maingate + row * self.cell_height_maingate
                x2 = x1 + self.cell_width_maingate
                y2 = y1 + self.cell_height_maingate
                self.maingate[row, col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="rect")

        self.canvas.create_text(self.init_x + 25, self.init_y - 10, text="PARKING")
        self.parking = {}
        for col in range(self.cols_pkg):
            for row in range(self.rows_pkg):
                x1 = self.init_x + col * self.cell_width
                y1 = self.init_y + row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                self.parking[row, col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="rect_pkg")

        self.canvas.create_text(self.init_x_est + 35, self.init_y_est - 10, text="ESTIBADORS")
        self.estibadors = {}
        for col in range(self.cols_est):
            for row in range(self.rows_est):
                x1 = self.init_x_est + col * self.cell_width_est
                y1 = self.init_y_est + row * self.cell_height_est
                x2 = x1 + self.cell_width_est
                y2 = y1 + self.cell_height_est
                self.estibadors[row, col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="rect")

    def run (self):
        self.redraw(self.delaySpeed)

    def setTraza (self, traza):
        self.traza = traza
        for i in range(len(self.traza)):
            st = self.traza[i]
            aux = st.split(",")
            self.traza_who.append(aux[0])
            self.traza_time.append(aux[1])
            self.traza_what.append(aux[2])
            if len(aux) > 3:
                self.traza_oper.append(aux[3])
                if len(aux) > 4:
                    self.traza_where.append(aux[4])
                else:
                    self.traza_where.append("-")
            else:
                self.traza_oper.append("-")
                self.traza_where.append("-")

    def getCurrentTime (self):
        return self.current_time

    def reset(self):
        self.current_time = -1
        self.iterator = 0
        self.setTerminal()

    def sPause (self):
        self.isPaused = not self.isPaused

    def updateSpeed (self, speed):
        self.delaySpeed = speed

    def redraw(self, delay):
        if not self.isPaused:
            self.current_time += 1
            while (len(self.traza) > self.iterator and str(self.current_time) == self.traza_time[self.iterator]):
                if self.traza_what[self.iterator] == "EXECUTAR":
                    if self.traza_oper[self.iterator] == "ARRIBADA":
                        if self.traza_where[self.iterator] != "MAINGATE":
                            aux = self.traza_who[self.iterator].split(" ")
                            row = 0
                            col = int(aux[3])
                            if int(aux[3]) >= 25:
                                col = col % 25
                                row = int(int(aux[3]) / 25)
                            item_id = self.parking[row,col]
                            self.canvas.itemconfig(item_id, fill="red")
                    else:
                        if self.traza_where[self.iterator] == "MAINGATE":
                            aux = self.traza_who[self.iterator].split(" ")
                            pos = int(aux[1])
                            item_id = self.maingate[int(pos), 0]
                            self.canvas.itemconfig(item_id, fill="blue")
                        elif self.traza_where[self.iterator] == "PARKING":
                            aux = self.traza_who[self.iterator].split(" ")
                            row = 0
                            col = int(aux[3])
                            if int(aux[3]) >= 25:
                                col = col % 25
                                row = int(int(aux[3])/ 25)
                            item_id = self.parking[row,col]
                            self.canvas.itemconfig(item_id, fill="green")
                        else:
                            aux = self.traza_who[self.iterator].split(" ")
                            row = 0
                            col = int(aux[1])
                            if int(aux[1]) >= 25:
                                col = col % 25
                                row = int(int(aux[1]) / 25)
                            item_id = self.estibadors[row,col]
                            self.canvas.itemconfig(item_id, fill="blue")
                elif self.traza_what[self.iterator] == "ENCUAR":  # queue
                    if self.traza_who[self.iterator] == "MAINGATE":
                        self.cua = self.traza_oper[self.iterator]
                        item_id = self.queue
                        self.canvas.itemconfig(item_id, text=self.cua)
                else:  # INICI SERVEI ESTIBADOR I MAINGATE
                    if self.traza_who[self.iterator][0] == "M":
                        aux = self.traza_who[self.iterator].split(" ")
                        pos = int(aux[1])
                        item_id = self.maingate[int(pos), 0]
                        self.canvas.itemconfig(item_id, fill="orange")
                    elif self.traza_who[self.iterator][0] == "E":
                        aux = self.traza_who[self.iterator].split(" ")
                        row = 0
                        col = int(aux[1])
                        if int(aux[1]) >= 25:
                            col = col % 25
                            row = int(int(aux[1]) / 25)
                        item_id = self.estibadors[row, col]
                        self.canvas.itemconfig(item_id, fill="yellow")

                # tracament de la traza
                if (self.delaySpeed == 1000):
                    sleep(0.01)
                self.iterator += 1

            if self.iterator == len(self.traza):
                self.isPaused = True
                self.setTerminal()

        self.canvas.after(self.delaySpeed, lambda :self.redraw(self.delaySpeed))
