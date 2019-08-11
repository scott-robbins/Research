import PIL.Image as Image
import Tkinter as Tk
import PIL.ImageTk
import time
import io


root = Tk.Tk()
canvas = Tk.Canvas(root, height=500, width=500)
tic = time.time()

img1 = Tk.PhotoImage(file='chess_board.png')
canvas.pack(expand=Tk.YES, fill=Tk.BOTH)
canvas.create_image(10, 10, image=img1, anchor=Tk.NW)   # put image on canvas
canvas.pack()

frame = Tk.Frame(root, width=100, height=100)
frame.pack()

root.mainloop()
