import Tkinter as tk
import reader
import os


def clear_clip():
    try:
        os.remove('clip.wav')
    except:
        pass


root = tk.Tk()
window = tk.Canvas(root, bg='#801cff', width=600, height=400)
window.pack()

start = tk.Button(window,text="Start", command=reader.start_recording)
start.place(x=100, y=200, relwidth=0.2, relheight=0.2)

stop = tk.Button(window,text="Stop", command=reader.stop_recording)
stop.place(x=200, y=200, relwidth=0.2, relheight=0.2)

play = tk.Button(window, text="Play", command=reader.play)
play.place(x=300, y=200, relwidth=0.2, relheight=0.2)

delete = tk.Button(window, text='Delete', command=clear_clip)
delete.place(x=400, y=200, relwidth=0.2, relheight=0.2)

root.mainloop()
