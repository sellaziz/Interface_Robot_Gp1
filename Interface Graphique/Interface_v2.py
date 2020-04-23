import matplotlib.pyplot as plt
import numpy as np
import math
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

class Interface():
    # VARIABLES
    FIGSIZE = (5, 4)
    DPI = 100
    DRAW_METHOD = 1

    def __init__(self):

        self.root = tkinter.Tk()
        self.root.wm_title("Interface Commande Robot")

        # Variables
        self.plt_draw = np.zeros((1,2))
        self.plt_draw[0] = np.array([0,1])
        self.command = np.zeros((1,2))
        self.command[0] = np.array([1,1])
        self.directions = np.array([[0,1]])

        self.setup()
        # print(self.plt_draw,"\n",self.plt_draw[:,0], self.plt_draw[:,1])
        self.drawing, = self.ax.plot(self.plt_draw[:, 0], self.plt_draw[:, 1])

        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect("button_press_event", self.on_key_press)

        self.set_buttons()

    def setup(self):
        self.fig = Figure(figsize=self.FIGSIZE, dpi=self.DPI)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

    def set_buttons(self):
        self.method_entry = tkinter.Entry(self.root)
        self.method_entry.pack(side=tkinter.TOP)

        self.update_methodbutton = tkinter.Button(master=self.root, text="Update", command=self.update_method)
        self.update_methodbutton.pack(side = tkinter.TOP)

        self.command_button = tkinter.Button(master=self.root, text="Command", command=self.print_command)
        self.command_button.pack(side = tkinter.TOP)

        self.quit_button = tkinter.Button(master=self.root, text="Quit", command=self._quit)
        self.quit_button.pack(side=tkinter.BOTTOM)

    def update_method(self):
        self.DRAW_METHOD = self.method_entry.get()
        print(self.DRAW_METHOD)

    def on_key_press(self, event):
        print("you pressed ({0},{1})".format(event.xdata, event.ydata))
        key_press_handler(event, self.canvas, self.toolbar)

        if self.DRAW_METHOD==1:
            x, y = event.xdata, event.ydata
            dv = x-self.plt_draw[-1][0] , y-self.plt_draw[-1][1]
            angle = self.get_ang(self.plt_draw[-1], np.array([x,y]), dir=True, direction=self.directions[-1])
            self.directions = np.vstack((self.directions, np.array(dv / np.linalg.norm(dv))))
            self.plt_draw = np.vstack((self.plt_draw, np.array([x,y])))
            if np.dot((self.directions[-1][0],0), (1,0))>0:
                angle = -angle
            if angle!=0:
                self.command = np.vstack((self.command, np.array([0,angle]))) # Rotation
            self.command = np.vstack((self.command, np.array([1,np.linalg.norm(dv)]))) # Ligne Droite


        # Update Canvas
        self.drawing.set_data(self.plt_draw[:, 0], self.plt_draw[:, 1])
        self.ax.figure.canvas.draw()

    def get_ang(self, v1, v2, dir=False, direction=(0,1)):
        vect1, vect2 = v1, v2
        if v1[0]==0 and v1[1]==0:
            vect1=np.array([0, 1])
            vect2 = v2
            dir=False
        if dir :
            vect2 = vect2-vect1
            vect1=direction
        v1_unit = vect1 / np.linalg.norm(vect1)
        v2_unit = vect2 / np.linalg.norm(vect2)
        dot_product = np.dot(v1_unit, v2_unit)
        return np.arccos(dot_product)

    def print_command(self):
        print(self.command)

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate



Interface()
tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
