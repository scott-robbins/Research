import PIL.Image as Image
import scipy.misc as misc
import Tkinter as tk
import PIL.ImageTk
import numpy as np
import imutils
import reader
import time
import os


def redraw(circ):
    dx = np.random.random_integers(-5, 5, 1)[0]
    dy = np.random.random_integers(-5, 5, 1)[0]
    window.after(100,redraw)
    window.move(circ, dx, dy)
    window.update()


def select(track):
    """ SELECT
    call back for selecting a song from the drop down menu.
    Title of the Tk Frame is updated to song title, and a
    shell command is called to play the given track and fork
    the process to background. Once a track is selected, and
    begins to play, the call to begin visualizer is made.
    :param track:
    :return:
    """
    sf = "track is %s" % var.get()
    root.title(sf)
    root['bg'] = var.set('blue')
    print 'Playing %s' % track
    os.system('paplay %s &' % track)
    # TODO: Music Visualization above track selection


def stop_playback():
    """
    Execute a shell command to find the process invoked for
    audio playback, and then kill it. There are some times
    children processes that need to be killed if multiple
    songs are chosen in series, or if a song is chosen before
    the first is finished playing, etc.
    :return:
    """
    cmd = 'ps aux | grep paplay | cut -b 10-16 | while read n; do kill -9 $n; done'
    os.system(cmd)


tic = time.time()
root = tk.Tk()
window = tk.Canvas(root, bg='#801cff', width=600, height=400)
window.pack()

# Find WAV Files
os.system('locate "*.wav" >> waves.txt')
os.system('locate "*.mp3" >> mp3s.txt')
wav_files = reader.swap('waves.txt', True)
mp3_files = reader.swap('mp3s.txt', True)

print '[*] %d WAV Files Found ' % len(wav_files)
print '[*] %d MP3 Files Found ' % len(mp3_files)
print '\033[1m[%ss Elapsed]\033[0m' % str(time.time()-tic)

var = tk.StringVar(root)
# initial value
var.set('Files')
choices = wav_files
option = tk.OptionMenu(root, var, *choices,command=select)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="stop", command=stop_playback)
button.pack(side='left', padx=20, pady=10)


root.mainloop()
