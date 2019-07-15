from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()

colors = {'R':[1,0,0],
          'G':[0,1,0],
          'B':[0,0,1],
          'C':[0,1,1],
          'M':[1,0,1],
          'Y':[1,1,0],
          'K':[0,0,0],
          'W':[1,1,1]}


def show_walk(c, movts, pos, state):
    walk = []
    f = plt.figure()
    state[pos[0],pos[1],:] = colors[c]
    walk.append([plt.imshow(state)])
    for step in movts:
        state[pos[0], pos[1], :] = 0
        state[step[0], step[1], :] = colors[c]
        pos = step
        walk.append([plt.imshow(state)])
    a = animation.ArtistAnimation(f,walk,interval=100,blit=True,repeat_delay=900)
    plt.show()


def show_cloud(c, n_points, n_steps, state):
    f = plt.figure()
    starting_points = []
    walks = {}
    for i in range(n_points):
        try:
            pos = imutils.spawn_random_point(state[:, :, 0])
            starting_points.append(pos)
            walks[i] = imutils.spawn_random_walk(pos, n_steps)
            state[pos[0], pos[1], :] = colors[c]
        except IndexError:
            pass

    k0 = [[1,1,1],[1,1,1],[1,1,1]]

    k1 = [[1,1,1,1,1],
          [1,2,2,2,1],
          [1,2,3,2,1],
          [1,2,2,2,1],
          [1,1,1,1,1]]

    walk = []
    walk.append([plt.imshow(state)])
    for step in range(n_steps):
        ind = 0
        new_positions = []
        for pt in starting_points:
            px = walks[ind][step]
            try:
                state[pt[0], pt[1], :] = [0, 0, 0]
                state[px[0], px[1], :] = colors[c]
            except IndexError:
                pass
            new_positions.append(px)
            ind += 1
        starting_points = new_positions
        #walk.append([plt.imshow(state)])
        # TODO: Now do second pass, and apply automata rules,
        #  then actually add THAT frame
        # ind2sub = imutils.LIH_flat_map_creator(state[:,:,0])
        rch = ndi.convolve(state[:,:,0], k1)
        gch = ndi.convolve(state[:,:,0], k0)
        bch = ndi.convolve(state[:,:,2], k1)
        for ii in range(len(new_positions)):
            state, starting_points = apply_rule(ii, state, rch, gch, bch, starting_points)
        state[:,:,0] += bch/(n_steps)
        state[:,:,1] += gch/(2*n_steps)
        walk.append([plt.imshow(state)])
    print '\033[1m\033[3mSIMULATION FINISHED \033[0m\033[1m[%ss Elapsed]\033[0m' % str(time.time()-tic)
    a = animation.ArtistAnimation(f, walk, interval=100, blit=True, repeat_delay=900)
    w = FFMpegWriter(fps=10,metadata=dict(artist='Me'),bitrate=1800)
    a.save('patter_generator_0.mp4',writer=w)
    plt.show()
    state[:,:,2] = np.zeros((state.shape[0],state.shape[1]))
    return state


def apply_rule(i, state, rch, gch, bch, points):
    x = points[i][0]
    y = points[i][1]
    try:
        if rch[x, y] >= 8:
            state[x, y, :] = [1, 1, 1]
    except IndexError:
        pass
    return state, points


n_pts = 500
steps = 150
width   = 150
height  = 150
canvas = np.zeros((width, height, 3))

if 'point' in sys.argv:
    start = [50, 50]
    movts = imutils.spawn_random_walk(start, steps)
    show_walk('R', movts, start, canvas)
else:
    final_image = show_cloud('B', n_pts, steps, canvas)
    plt.close()
    plt.show(final_image)
    plt.title('Final State')
    plt.imshow(final_image)
    plt.show()