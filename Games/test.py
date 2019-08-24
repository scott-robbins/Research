import Tkinter as Tk
import PIL.ImageTk
import PIL.Image as Image
import time
import io

root = Tk.Tk()
canvas = Tk.Canvas(root, height = 500, width = 500)
tic = time.time()

# Create two images
R = PIL.Image.open("red_box.png")
G = PIL.Image.open("green_box.png")
B = PIL.Image.open("blue_box.png")

imR = R.resize((80, 80))
imG = G.resize((80, 80))
imB = B.resize((80, 80))
rim = PIL.ImageTk.PhotoImage(imR)
gim = PIL.ImageTk.PhotoImage(imG)
bim = PIL.ImageTk.PhotoImage(imB)
rbox = canvas.create_image(100, 100, image=rim, tags="red")
gbox = canvas.create_image(100, 250, image=gim, tags="green")
bbox = canvas.create_image(100, 400, image=bim, tags="blue")
images = [rbox, gbox, bbox]


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
            id = getImage(rim, event.x, event.y)
            if id:
                canvas.coords(id, (event.x, event.y))


# Binding
canvas.bind("<B1-Motion>", click)
# Place the rectangle on top of all
canvas.pack()


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


def enter(event):
    print '[Enter]'


frame = Tk.Frame(root, width=100, height=100)

''' GET ARROW KEY BINDINGS [L D R U] '''
root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Down>', downKey)
root.bind('<Up>', upKey)
root.bind('<Return>', enter)
frame.pack()

''' RUN MAIN LOOP '''
root.mainloop()
