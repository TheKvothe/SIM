from Canvas import Canvas
import tkinter



class GUI:
    def __init__(self):
        self.canvs = None
        self.traza = []
        self.mainWindow = tkinter.Tk()
        self.mainWindow.title("Terminal APMT")

        self.isPause = True
        self.delaySpeed = 1000

        self.width_of_window = 1250
        self.height_of_window = 550

        self.screen_width = self.mainWindow.winfo_screenwidth()
        self.screen_height = self.mainWindow.winfo_screenheight()

        self.x_coordinate = (self.screen_width / 2) - (self.width_of_window / 2)
        self.y_coordinate = (self.screen_height / 2) - (self.height_of_window / 2)

        self.mainWindow.geometry("%dx%d+%d+%d" % (self.width_of_window, self.height_of_window, self.x_coordinate, self.y_coordinate))

        # Menu Basico TOP
        self.TopFrame = tkinter.Frame(self.mainWindow, width=1250, height=100, borderwidth=1)
        self.TopFrame.pack()

        def slow():
            self.delaySpeed *= 2
            self.cnvs.updateSpeed(self.delaySpeed)
            print("SLOW")

        def sPause():

            self.isPause = not self.isPause

        def fast():
            self.delaySpeed /= 2
            self.cnvs.updateSpeed(self.delaySpeed)

            print(self.delaySpeed)

        self.slow = tkinter.Button(self.TopFrame, text="Slow",command=slow)
        self.play = tkinter.Button(self.TopFrame, text="Play",command=sPause)
        self.fast = tkinter.Button(self.TopFrame, text="Fast",command=fast)

        self.slow.grid(column=0, row=0)
        self.play.grid(column=1, row=0)
        self.fast.grid(column=2, row=0)

        
        self.cnvs = Canvas(self.mainWindow, self.delaySpeed)
        self.time = tkinter.Label(self.TopFrame, text=self.cnvs.getCurrentTime())
        self.time.grid(column=3, row=0)
        self.update_timer(self.delaySpeed)



    def setTraza(self, traza):
        self.traza = traza
        self.cnvs.setTraza(traza)
        self.cnvs.run()

    def update_timer(self,delay):
        self.time = tkinter.Label(self.TopFrame, text=self.cnvs.getCurrentTime())
        self.time.grid(column=3, row=0)
        self.time.after(self.delaySpeed, lambda:self.update_timer(self.delaySpeed))

    def run(self):
        self.mainWindow.mainloop()

