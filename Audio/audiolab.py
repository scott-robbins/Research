from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy.io import wavfile
import Tkinter as tk
import PIL.ImageTk
import numpy as np
import imutils
import reader
import time
import os


class Cloud:
    particles = {}
    n_points = 0
    positions = {}
    sz = 10
    state = []
    W = 0
    H = 0

    def __init__(self, audio_label, canv, dim):
        self.W = dim[0]
        self.H = dim[1]
        raw_audio = self.pre_process_audio(audio_label)
        self.initialize(raw_audio, canv)

    def pre_process_audio(self, track):
        sample_rate, audio = wavfile.read(track)
        audio = np.array(audio)
        if sample_rate == 48000:
            self.W = 240
            self.H = 400
        print '[*] Sample Rate: %d' % sample_rate
        print '[*] Raw Audio Shape: %s' % str(audio.shape)
        self.runtime_sec = audio.shape[0]/float(sample_rate)
        ''' Want to process the audio data one second at a time '''
        self.sample_rate = sample_rate
        return audio

    def initialize(self, data, canvas):
        animation = []
        f = Figure(figsize=(5, 3), dpi=100)
        a = f.add_subplot(111)
        self.frame = FigureCanvasTkAgg(f, master=canvas)
        ''' VISUALIZATION '''
        self.state = data[0:self.sample_rate].reshape((self.W, self.H))
        animation.append([a.imshow(self.state)])
        print 'Running Visualization of %s Seconds ' % str(self.runtime_sec)
        for sec in range(int(self.runtime_sec)):
            self.state = data[self.sample_rate*sec:self.sample_rate*sec+self.sample_rate].reshape((self.W, self.H))
            animation.append([a.imshow(self.state)])
            self.frame.draw()
            self.frame.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.frame._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        a = animation.ArtistAnimation(f, animation, interval=750, blit=True, repeat_delay=900)
        plt.show()

        a.imshow(self.state, 'gray')



# GLOBALS [ :( ]
tic = time.time()
root = tk.Tk()
window = tk.Canvas(root, bg='#801cff', width=600, height=400)
window.pack()


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
    visual = Cloud(track, window, [210, 420])


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


if __name__ == '__main__':

    # Find WAV Files
    os.system('locate "*.wav" >> waves.txt')
    os.system('locate "*.mp3" >> mp3s.txt')
    wav_files = reader.swap('waves.txt', True)
    mp3_files = reader.swap('mp3s.txt', True)   # TODO: Make MP3s available

    print '[*] %d WAV Files Found ' % len(wav_files)
    print '[*] %d MP3 Files Found ' % len(mp3_files)
    print '\033[1m[%ss Elapsed]\033[0m' % str(time.time() - tic)

    var = tk.StringVar(root)
    # initial value
    var.set('Files')
    choices = wav_files
    option = tk.OptionMenu(root, var, *choices, command=select)
    option.pack(side='left', padx=10, pady=10)
    button = tk.Button(root, text="stop", command=stop_playback)
    button.pack(side='left', padx=20, pady=10)




    root.mainloop()

