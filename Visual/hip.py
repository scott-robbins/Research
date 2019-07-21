from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()

colors = {'R': [1,0,0],
          'G': [0,1,0],
          'B': [0,0,1],
          'C': [0,1,1],
          'M': [1,0,1],
          'Y': [1,1,0],
          'K': [0,0,0],
          'W': [1,1,1]}


def generate_seed_state(width, height, d, show):
    state = np.zeros((width, height))
    n_pts = int((d*width*height) / 3)
    print 'Using %d Points for seeding' % n_pts

    for pt in range(n_pts):
        [x, y] = imutils.spawn_random_point(state)
        seed = np.random.random_integers(0,1,16).reshape((4,4))
        try:
            state[x-2:x+2, y-2:y+2] = seed
        except IndexError:
            pass
        except ValueError:
            pass
    if show:
        # Check Initial State
        plt.title('Initial State')
        plt.imshow(state, 'gray')
        plt.show()
    return state


def simple_sime(depth, WIDTH, HEIGHT):
    f = plt.figure()
    simulation = []
    simulation.append([plt.imshow(seed, 'gray')])
    flipped = np.zeros((WIDTH, HEIGHT))
    for step in range(depth):
        c0 = ndi.convolve(seed, net_0)
        c1 = ndi.convolve(seed, net_1)
        c2 = ndi.convolve(seed, net_2)
        for y in range(seed.shape[0]):
            for x in range(seed.shape[1]):
                px = seed[x, y]
                if flipped[x, y] > depth - depth / 2:
                    seed[x, y] = 0
                if px == 1:
                    if (c0[x, y] or c1[x, y]) % 4 == 0:
                        seed[x, y] = 0
                        flipped[x, y] += 1
                    if 8 > (c1[x, y]) >= 4:
                        seed[x, y] = 1
                        flipped[x, y] += 1
                    if (c0[x, y] or c1[x, y]) >= 8:
                        seed[x, y] = 0
                        flipped[x, y] += 1
                elif px == 0:
                    if (c1[x, y] == 4) or c0[x, y] == 8:
                        seed[x, y] = 1
                        flipped[x, y] += 1
                if c2[x, y] > 10:
                    seed[x, y] = 0
        simulation.append([plt.imshow(seed, 'gray')])
    print 'SIMULATION FINISHED [%ss Elapsed]' % str(time.time() - tic)
    a = animation.ArtistAnimation(f, simulation, interval=70, blit=True, repeat_delay=900)
    if save:
        w = FFMpegWriter(fps=20, metadata=dict(artist='Me'), bitrate=1800)
        a.save(save_name, writer=w)
    plt.show()


length = 250
W = 250
H = 250
density = 0.0025
seed = np.zeros((W, H))
seed[50:200, 50:200] = generate_seed_state(150, 150, density, False)
seed[150:200,150:200] = imutils.draw_centered_circle(np.zeros((50, 50)), 10,1,False)
seed = np.abs(seed)
net_0 = [[0,0,0,0],
         [0,2,2,0],
         [0,2,2,0],
         [0,0,0,0]]

net_1 = [[0,0,0,0,0,0],
         [0,0,1,1,0,0],
         [0,1,1,1,1,0],
         [0,1,1,1,1,0],
         [0,0,1,1,0,0],
         [0,0,0,0,0,0]]

net_2 = [[0,0,0,0,0,0,0],
         [0,0,1,0,1,0,0],
         [0,1,1,1,1,1,0],
         [0,0,1,0,1,0,0],
         [0,1,1,1,1,1,0],
         [0,0,1,0,1,0,0]]

# f, ax = plt.subplots(1, 3, sharey=True,sharex=True)
# ax[0].imshow(seed, 'gray')
# ax[1].imshow(ndi.convolve(seed,net_0), 'gray')
# ax[2].imshow(ndi.convolve(seed, net_1), 'gray')
# plt.show()

# RUN SIMULATION
save_name = ''
save = False
if len(sys.argv) ==3 and '-s' in sys.argv:
    save_name = sys.argv[2]
    save = True
# RUN IT
simple_sime(length, W, H)
