from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import PIL.Image as Image
import Tkinter as Tk
import numpy as np
import imutils
import engine
import time
import sys


tic = time.time()
width = 250
height = 250
world = np.zeros((width, height, 3))
start = imutils.spawn_random_point(world[:, :, 0])
Point = engine.particle(start)
world[Point.x-3:Point.x, Point.y-3:Point.y, 2] = 1

root = Tk.Tk()
root.wm_title("Embedding in TK")


# ##### ###################### [| * ~ Figure Methods ~ * |] ###################### ##### #
def on_click(event):
    [x, y] = [int(event.xdata), int(event.ydata)]
    print '[%s, %s]' % (str(x), str(y))
    Point.update(x, y)
    world[Point.x - 3:Point.x, Point.y - 3:Point.y, 2] = 1
    a.imshow(world)


def update_pos(event):
    a.cla()
    try:
        world[Point.x, Point.y, :] = 0
        x = event['x']
        y = event['y']
        Point.update(x, y)
        world[Point.x - 3:Point.x, Point.y - 3:Point.y, 2] = 1
    except IndexError:
        return
    a.imshow(world)
    Point.show()
    plt.show()


def leftKey(event):
    print "< Left key pressed"
    if type(event) != 'MouseEvent':
        update_pos({'x':-1,'y':0})


def rightKey(event):
    print ">  Right key pressed"
    if type(event) != 'MouseEvent':
        update_pos({'x': 1,'y': 0})


def downKey(event):
    print "v Down"
    if type(event) != 'MouseEvent':
        update_pos({'x': 0,'y': 1})


def upKey(event):
    print '^ Up '
    if type(event) != 'MouseEvent':
        update_pos({'x':0,'y': -1})

# ##### ###################### [| * ~ Figure Methods ~ * |] ###################### ##### #


f = Figure(figsize=(10, 8), dpi=100)
a = f.add_subplot(111)
a.grid()
a.imshow(world)
plt.show()

b0 = Tk.Button(master=root, text='Quit', command=sys.exit)
b0.place(x=0,y=0,relwidth=0.1,relheight=0.1)

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=0, y=100, relwidth=1, relheight=0.8)
canvas._tkcanvas.place(x=100, y=100, relwidth=0.8, relheight=0.8)

f.canvas.callbacks.connect('button_press_event', on_click)
''' GET ARROW KEY BINDINGS [L D R U] '''
root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Down>', downKey)
root.bind('<Up>', upKey)


# RUN IT
Tk.mainloop()
