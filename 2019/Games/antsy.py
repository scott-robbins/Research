import Tkinter as Tk
import PIL.ImageTk
import PIL.Image as Image
import numpy as np
import imutils
import time

root = Tk.Tk()
canvas = Tk.Canvas(root, height = 500, width = 500)
tic = time.time()

cell_file = PIL.Image.open("box.png")
cell_mat = cell_file.resize((100, 100))
cell_im = PIL.ImageTk.PhotoImage(cell_mat)
cell = canvas.create_image(100, 100, image=cell_im, tags='cell')

# Create ANT Object(s)
ant_start = imutils.spawn_random_point(np.zeros((500, 500)))
ant_file = PIL.Image.open("ant.png")
ant_mat = ant_file.resize((20, 35))
ant_im = PIL.ImageTk.PhotoImage(ant_mat)
ant = canvas.create_image(ant_start[0], ant_start[1],image=ant_im,tags='ant')
images = [cell]


def getImage(imagePI, x, y):
    for image in images:
        curr_x, curr_y = canvas.coords(image)
        x1 = curr_x - imagePI.width()/2
        x2 = curr_x + imagePI.width()/2
        y1 = curr_y - imagePI.height()/2
        y2 = curr_y + imagePI.height()/2
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            return image


def click(event):
    # print "clicked at", event.x, event.y
    for image in images:
        curr_x, curr_y = canvas.coords(image)
        if abs(event.x-curr_x) <= 50 and abs(event.y-curr_y) <= 50:
            # Here I select image1 or image2 depending on where I click, and
            # drag them on the canvas. The problem is when I put the rectangle
            # on top using tag_raise (see below).
            id = getImage(cell_im, event.x, event.y)
            if id:
                canvas.coords(id, (event.x, event.y))


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


# Binding
canvas.bind("<B1-Motion>", click)
# Place the rectangle on top of all
canvas.pack()

frame = Tk.Frame(root, width=100, height=100)

''' GET ARROW KEY BINDINGS [L D R U '''
root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Down>', downKey)
root.bind('<Up>', upKey)
# root.bind('<Return>', snapshot)
frame.pack()

print 'Press Enter To Save Workspace... '

''' RUN MAIN LOOP '''
root.mainloop()
