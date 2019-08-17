from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import PIL.Image as Image
import Tkinter as Tk
import numpy as np
import PIL.ImageTk
import time
import sys

def destroy(e):
    sys.exit()


# def getImage(imagePI, x, y):
#     for image in images:
#         curr_x, curr_y = canvas.coords(image)
#         x1 = curr_x - imagePI.width()/2
#         x2 = curr_x + imagePI.width()/2
#         y1 = curr_y - imagePI.height()/2
#         y2 = curr_y + imagePI.height()/2
#         if (x1 <= x <= x2) and (y1 <= y <= y2):
#             return image


def leftKey(event):
    print "< Left key pressed"
    click(event)


def rightKey(event):
    print ">  Right key pressed"
    click(event)


def downKey(event):
    print "v Down"
    click(event)


def upKey(event):
    print '^ Up '
    click(event)


def click(event):
    print "clicked at", event.x, event.y


def run():
    tic = time.time()
    root = Tk.Tk()
    root.wm_title("Embedding in TK")

    f = Figure(figsize=(5, 4), dpi=100)
    a = f.add_subplot(111)

    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2 * np.pi * t)

    a.plot(t, s)
    a.set_title('Tk embedding')
    a.set_xlabel('X axis label')
    a.set_ylabel('Y label')

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    button = Tk.Button(master=root, text='Quit', command=sys.exit)
    button.pack(side=Tk.BOTTOM)

    Tk.mainloop()


w = 250
h = 250
state = np.zeros((w, h))
