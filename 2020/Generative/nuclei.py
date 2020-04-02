from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
from tqdm import tqdm
import numpy as np
import imutils
import time
import sys
import os


k0 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
k1 = [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]]
r = [1,0,0]; g = [0,1,0]; b = [0,0,1]
c = [0,1,1]; m = [1,0,1]; y = [1,1,0]
k = [0,0,0]; w = [1,1,1]

colors = {'r': r, 'g': g, 'b': b,
          'c': c, 'm': m, 'y': y,
          'k': k, 'w': w}


def torch(seed, limits, generations):
    # Made with limits: [4,3,0]/probabilities:[1,1,0
    tic = time.time()
    f = plt.figure()
    simulation = []
    simulation.append([plt.imshow(seed)])

    rlim = limits[0]
    glim = limits[1]
    blim = limits[2]

    dimensions = [seed.shape[0], seed.shape[1]]
    ind2sub = imutils.ind2sub(dimensions)
    for generation in tqdm(range(generations)):
        rch = ndi.convolve(seed[:,:,0], k1, origin=0)
        gch = ndi.convolve(seed[:,:,1], k1, origin=0)
        bch = ndi.convolve(seed[:,:,2], k1, origin=0)
        for ii in range(seed.shape[0]*seed.shape[1]):
            [x, y] = ind2sub[ii]
            if seed[x,y,0]==1 and (seed[x,y,1] and seed[x,y,2])==0:  # red
                if gch[x,y] % glim == 1:
                    seed[x,y,1] = 0
                if rch[x,y] % rlim == 1:
                    seed[x,y,0] = 0
            elif seed[x,y,1]==1 and (seed[x,y,0] and seed[x,y,2])==0:  # green
                if rch[x,y] % rlim == 1:
                    seed[x,y,0] = 0
                if gch[x,y] % glim == 1:
                    seed[x, y, 1] = 0
            elif seed[x,y,2]==1 and (seed[x,y,0] and seed[x,y,1])==0:  # blue:
                if gch[x,y] % glim == 1:
                    seed[x, y, 1] = 0
                if rch[x,y] % rlim == 1:
                    seed[x,y,0] = 0
            elif (seed[x,y,0] and seed[x,y,1] and seed[x,y,2])==0:  # black
                if rch[x,y] > rlim:
                    seed[x,y,:] = r
                if gch[x,y] > glim:
                    seed[x,y,:] = g
                if bch[x,y] > blim:
                    seed[x,y,:] = b
        simulation.append([plt.imshow(seed)])
    print '[*] Simulation Finished [%ss Elapsed]' % str(time.time()-tic)
    a = animation.ArtistAnimation(f,simulation,interval=100,blit=True,repeat_delay=900)
    plt.show()
    return seed  # return the final state


def run(seed, limits, probabilities, generations):
    tic = time.time()
    f = plt.figure()
    simulation = []
    simulation.append([plt.imshow(seed)])

    rlim = limits[0]; rhit = probability[0]*100
    glim = limits[1]; ghit = probability[1]*100
    blim = limits[2]; bhit = probability[2]*100

    dimensions = [seed.shape[0], seed.shape[1]]
    ind2sub = imutils.ind2sub(dimensions)
    white_pxls = np.zeros(dimensions)
    cutoff = 100
    print '\033[1m[*] Starting Simulation\033[32m'
    for generation in tqdm(range(generations)):
        rch = ndi.convolve(seed[:,:,0], k1, origin=0)
        gch = ndi.convolve(seed[:,:,1], k1, origin=0)
        bch = ndi.convolve(seed[:,:,2], k1, origin=0)
        rflip = np.random.random_integers(1, 100, 1)[0]
        gflip = np.random.random_integers(1, 100, 1)[0]
        bflip = np.random.random_integers(1, 100, 1)[0]

        for ii in range(seed.shape[0]*seed.shape[1]):
            [x, y] = ind2sub[ii]

            if seed[x,y,0]==1 and (seed[x,y,1] and seed[x,y,2])==0:  # red
                if gch[x,y] % glim == 1:
                    seed[x,y,1] = 1
                elif rch[x,y] % rlim == 1:
                    seed[x,y,0] = 0
                if bch[x,y] >=3:
                    seed[x,y,:] = 0
            elif seed[x,y,1]==1 and (seed[x,y,0] and seed[x,y,2])==0:  # green
                if gch[x,y] % glim == 1:
                    seed[x, y, 1] = 0
                elif rch[x,y] % rlim == 1:
                    seed[x,y,0] = 0
                if bch[x,y] >=2:
                    seed[x,y,:] = 0
            elif seed[x,y,2]==1 and (seed[x,y,0] and seed[x,y,1])==0:  # blue:
                if gch[x,y] % glim == 1:
                    seed[x, y, 1] = 0
                elif rch[x,y] % rlim == 1:
                    seed[x,y,0] = 0

            elif seed[x,y,2]==0 and (seed[x,y,0] and seed[x,y,1])==1:   # yellow
                if rch[x,y]>rlim and gch[x,y]>glim:
                    seed[x,y,:] = [1,1,0]
            elif (seed[x,y,0] and seed[x,y,1] and seed[x,y,2])==0:  # black
                if rch[x,y] >rlim and gch[x,y]>glim:
                    seed[x,y,:] = [1,1,0]
                elif rch[x,y] > rlim and rflip<=rhit:
                    seed[x,y,:] = [1,0,0]
                elif gch[x,y] > glim and gflip<=ghit:
                    seed[x,y,:] = [0,1,0]
                elif bch[x,y] > blim and bflip<=bhit:
                    seed[x,y,:] = [0,0,1]

        simulation.append([plt.imshow(seed)])
    print '\033[0m\033[1m[*] Simulation Finished [%ss Elapsed]\033[0m' % str(time.time()-tic)
    a = animation.ArtistAnimation(f,simulation,interval=100,blit=True,repeat_delay=900)
    w = FFMpegWriter(fps=30,bitrate=3200)
    a.save('boundary_condition_3.mp4',writer=w)
    plt.show()
    return seed  # return the final state


# Display Settings
W = 300
H = 300
initial_state = np.zeros((W, H, 3))
sz = 25
cx = int(W/2)
cy = int(H/2)

x1 = cx - sz;   x2 = cx + sz
y1 = cy - sz;   y2 = cy + sz

boundx1 = x1 - 100; boundx2 = x2 + 100
boundy1 = y1 - 100; boundy2 = y2 + 100

initial_state[boundy1:boundy2, boundx1,:] = b
initial_state[boundy1:boundy2, boundx2,:] = b
initial_state[boundy1, boundx1:boundx2,:] = b
initial_state[boundy2, boundx1:boundx2,:] = b
initial_state[(x1-sz):(x2+sz), (y1-sz):(y2+sz), :] = r
initial_state[(x1-sz/3):(x2+sz/3), (y1-sz/3):(y2+sz/3), :] = g

# Add some Gas in the box
dx = boundx2 - boundx1
dy = boundy2 - boundy1
# Simulation Parameters
density = [3, 4, 5]  # Limits on [R G B]
probability = [0.4, 0.3, 0.01]
n_generations = 200
# Run it
run(initial_state, density, probability, n_generations)