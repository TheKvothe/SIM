from Canvas import Canvas
import tkinter



class GUI:
    def __init__(self):
        self.canvs = None
        self.traza = []
        self.mainWindow = tkinter.Tk()
        self.mainWindow.title("Terminal APMT")

        self.delaySpeed = 1000
        self.isPaused = True

        self.width_of_window = 1000
        self.height_of_window = 500

        self.screen_width = self.mainWindow.winfo_screenwidth()
        self.screen_height = self.mainWindow.winfo_screenheight()

        self.x_coordinate = (self.screen_width / 2) - (self.width_of_window / 2)
        self.y_coordinate = (self.screen_height / 2) - (self.height_of_window / 2)

        self.mainWindow.geometry("%dx%d+%d+%d" % (self.width_of_window, self.height_of_window, self.x_coordinate, self.y_coordinate))

        # Menu Basico TOP
        self.TopFrame = tkinter.Frame(self.mainWindow, width=1250, height=50, borderwidth=1)
        self.TopFrame.pack()

        def slow():
            self.delaySpeed *= 2
            self.delaySpeed = int(self.delaySpeed)
            self.cnvs.updateSpeed(self.delaySpeed)

        def sPause():
            self.cnvs.sPause()
            self.isPaused = not self.isPaused

        def fast():
            if self.delaySpeed > 1:
                self.delaySpeed /= 2
                self.delaySpeed = int(self.delaySpeed)
                self.cnvs.updateSpeed(self.delaySpeed)

        def reset():
            self.cnvs.reset()

        self.slow = tkinter.Button(self.TopFrame, text="Slow",command=slow)
        self.play = tkinter.Button(self.TopFrame, text="Play/Pause",command=sPause)
        self.fast = tkinter.Button(self.TopFrame, text="Fast",command=fast)
        self.reset = tkinter.Button(self.TopFrame, text="Reset", command=reset)
        self.slow.grid(column=0, row=0, padx=5)
        self.play.grid(column=1, row=0, padx=5)
        self.fast.grid(column=2, row=0, padx=5)
        self.reset.grid(column=3, row=0, padx=5)

        self.cnvs = Canvas(self.mainWindow, self.delaySpeed)
        self.time = tkinter.Label(self.TopFrame, text=self.cnvs.getCurrentTime(), font="Times 20")
        self.time.grid(column=4, row=0, padx=700)
        self.update_timer(self.delaySpeed)

    def setTraza(self, traza):
        self.traza = traza
        self.cnvs.setTraza(traza)


    def update_timer(self,delay):
        if not self.isPaused:
            self.time = tkinter.Label(self.TopFrame, text=self.cnvs.getCurrentTime(), font="Times 20")
            self.time.grid(column=4, row=0, padx=700)
        self.time.after(self.delaySpeed, lambda: self.update_timer(self.delaySpeed))

    def run(self):
        self.cnvs.run()
        self.mainWindow.mainloop()

