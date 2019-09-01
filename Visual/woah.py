import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import os

# TODO: ASCII Art Splash while things load up

tic = time.time()
file_name_out = 'color_automata_simulation_0.mp4'
ani_cmd = 'ffmpeg -loglevel quiet -r 10 -i img%d.png -vcodec libx264 -pix_fmt yuv420p ' + file_name_out
clean = 'ls *.png | while read n; do rm $n; done'

k0 = [[1,1,1],
      [1,0,1],
      [1,1,1]]

k1 = [[1,1,1,1],
      [1,0,0,1],
      [1,0,0,1],
      [1,1,1,1]]

k2 = [[0,0,0,0],
      [0,1,1,0],
      [0,1,1,0],
      [0,0,0,0]]

# Simulation Parameters
width = 250
height = 250
depth = 100
world = np.zeros((width, height, 3))
# Constructing a basic color world to build from
world[:,:,0] = imutils.draw_centered_circle(np.zeros((width, height)), (width/3), 1, False)
world[:,:,2] = imutils.draw_centered_box(np.zeros((width, height)), (width/2),1,False)
pts = imutils.LIH_flat_map_creator(np.zeros((width, height)))
print '\033[1m\033[33m\0Ready to run Simulation! [%ss Elapsed]\033[0m' % str(time.time()-tic)

''' RUN SIMULATION '''
f = plt.figure()
simulation = []
simulation.append([plt.imshow(world)])
for frame in range(depth):
    rch = world[:,:,0]
    bch = world[:,:,1]
    gch = world[:,:,2]

    er1 = ndi.convolve(world[:,:,0], k1, origin=0).flatten()
    er2 = ndi.convolve(world[:,:,0], k2, origin=0).flatten()
    eg1 = ndi.convolve(world[:, :, 1], k1, origin=0).flatten()
    eg2 = ndi.convolve(world[:, :, 1], k2, origin=0).flatten()
    eb1 = ndi.convolve(world[:, :, 2], k1, origin=0).flatten()
    eb2 = ndi.convolve(world[:, :, 2], k2, origin=0).flatten()

    ri = 0
    bi = 0
    gi = 0
    for rpt in er1:
        [x,y] = pts[ri]
        if rpt % 3 == 0 and er2[ri]==4:
            world[x,y,0] = 0
        if rpt % 4 == 0 and gch[x,y] == 1:
            world[x, y, 0] = 1
            world[x, y, 2] = 0
        ri += 1

    for gpt in np.array(gch).flatten():
        [x, y] = pts[gi]
        if (rch[x, y] and bch[x, y] and gch[x, y]) == 1:
            if er1[gi] > 5:
                world[x, y, 0] = 0
                world[x, y, 1] = 1
                world[x, y, 2] = 0
        gi += 1
    for bpt in np.array(bch).flatten():
        [x, y] = pts[bi]
        if eb1[bi] % 6 == 0 and er2[bi] ==4:
            world[x, y, 2] = 0
            world[x, y, 0] = 1
        if (rch[x, y] and bch[x, y] and gch[x, y]) == 0:
            if er1[bi] > 5:
                world[x, y, 0] = 1
                world[x, y, 1] = 1
        bi += 1
    simulation.append([plt.imshow(world)])
    misc.imsave('img'+str(frame)+'.png', world)
print '\033[1mSIMULATION FINISHED [%ss Elapsed]' % str(time.time()-tic)
print '\033[3mRendering...\033[0m'
a = animation.ArtistAnimation(f,simulation,interval=300,blit=True,repeat_delay=900)
plt.show()

if raw_input('Want to save animation? (y/n): ').upper() == 'Y':
    os.system(ani_cmd)
    os.system('vlc %s' % file_name_out)
os.system(clean)