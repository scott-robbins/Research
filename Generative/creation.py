from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()

p0 = [[0,0,0,1],
      [0,1,0,0],
      [0,0,1,0],
      [1,0,0,0]]

p1 = [[0,1,1,0],
      [1,0,0,1],
      [1,0,0,1],
      [0,1,1,0]]

p2 = [[0,0,0,0],
      [0,1,1,0],
      [0,1,1,0],
      [0,0,0,0]]

p3 = [[0,1,1,0],
      [1,1,1,1],
      [1,1,1,1],
      [0,1,1,0]]

p4 = [[1,0,0,0,1],
      [0,1,2,1,0],
      [0,2,1,2,0],
      [0,1,2,1,0],
      [1,0,0,0,1]]


def cli_splash(n, N):
    os.system('clear')
    print '='*60
    print ' ____  ___    ======  ___ '
    print '|  __|| _ \\  | |__  | D |'
    print '| |   ||_| | | __|    _  |'
    print '| |__ | |\\ \\ | |___ | | | |'
    print '|____||_| \\_\\|_____||_| |_|'
    print ''
    print '[%ss Elapsed]\t%s Percent Complete' % (str(time.time()-tic), str(float(100.*n/N)))
    print '='*int(60.*n/N)


def sim0(state, depth, save):
    f = plt.figure()
    film = []
    ind2sub = imutils.flat_map_creator(state)
    shapes = {1: p0, 2: p1, 3: p2, 4: p3, 5: p4}
    film.append([plt.imshow(state)])
    for step in range(depth):
        k = np.array(shapes[np.random.random_integers(1, 5, 1)[0]])
        cnv = ndi.convolve(state, k, origin=0)
        cli_splash(step, depth)
        for ii in range(state.shape[0]*state.shape[1]):
            [x, y] = ind2sub[ii]
            if cnv[x,y] % 4 == 0:
                state[x,y] -= 1
            if cnv[x,y] % -4 == 0:
                state[x,y] += 1
            if cnv[x,y] % 5 == 0:
                state[x, y] -= 1
            if cnv[x,y] % -5 == 0:
                state[x, y] += 1
            if cnv[x,y] % 14 == 0:
                state[x,y] += 3
            if cnv[x,y] % 15 == 0:
                state[x, y] -= 3
            if state[x,y] % 29 == 0 and state[x,y]>0 and cnv[x,y] % 4 == 0:
                state[x,y] = 0
            if state[x,y] and cnv[x,y] % 29 == 0:
                state[x,y] = 0

        # film.append([plt.imshow(state, 'gray')])
        film.append([plt.imshow(state)])

    ''' Animate the Simulation '''
    a = animation.ArtistAnimation(f, film, blit=True, interval=save['frame_rate'], repeat_delay=900)
    if save['save']:
        writer = FFMpegWriter(fps=save['frame_rate'], bitrate=1800)
        a.save(save['name'], writer)
    print 'Simulation FINISHED\t[%ss Elapsed]' % str(time.time()-tic)
    plt.show()


def sim1(state, depth, save):
    f = plt.figure()
    film = []
    ind2sub = imutils.flat_map_creator(state)
    shapes = {1: p0, 2: p1, 3: p2, 4: p3, 5: p4}
    film.append([plt.imshow(state)])

    ''' Run the Simulation '''
    for step in range(depth):
        for ii in range(state.shape[0] * state.shape[1]):
            [x, y] = ind2sub[ii]

        film.append([plt.imshow(state)])

    ''' Animate the Simulation '''
    a = animation.ArtistAnimation(f, film, blit=True, interval=save['frame_rate'], repeat_delay=900)
    if save['save']:
        writer = FFMpegWriter(fps=save['frame_rate'], bitrate=1800)
        a.save(save['name'], writer)
    print 'Simulation FINISHED\t[%ss Elapsed]' % str(time.time() - tic)
    plt.show()


if __name__ == '__main__':
    w = 250
    h = 250
    depth = 150
    initial_state = imutils.draw_centered_circle(np.zeros((w, h)), w / 3, 255, False)
    initial_state -= imutils.draw_centered_box(np.zeros((w, h)), w / 4, 128, False)
    # initial_state = abs(initial_state-imutils.draw_centered_box(np.zeros((w, h)), w/4, 128, False))
    opts = {'save': False, 'frame_rate': 10}

    if '-i' in sys.argv:
        initial_state = np.array(plt.imread(sys.argv[2])).astype(np.float)
        if len(initial_state.shape) == 3:
            initial_state = initial_state[:,:,2]
            opts = {'save': True,
                    'frame_rate': 45,
                    'name': sys.argv[2].split('.')[0]+'_sim.mp4'}
    print '\033[1m\t\t<<_Starting_Simulation_>>\033[0m'
    if '-0' in sys.argv:
        sim0(initial_state, depth, opts)
    if '-1' in sys.argv:
        sim1(initial_state, depth, opts)
