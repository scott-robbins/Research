import tkinter as tk
import numpy as np
import time

x = np.random.random_integers(0, 300, 1)[0]
y = np.random.random_integers(0, 300, 1)[0]
size = 20
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
circle = canvas.create_oval(x-size, y-size, x+size, y+size, outline="white",fill="blue")


def redraw():
    dx = np.random.random_integers(-5, 5, 1)[0]
    dy = np.random.random_integers(-5, 5, 1)[0]
    canvas.after(100,redraw)
    canvas.move(circle, dx, dy)
    canvas.update()
redraw()
root.mainloop()