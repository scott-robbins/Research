import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()

R_THRESH = 20
G_THRESH = 20
B_THRESH = 20

k0 = [[1,1,1], [1,0,1], [1,1,1]]
k1 =[[0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]]
ani_cmd = 'ffmpeg -loglevel quiet -r 5 -i pic%d.png -vcodec libx264 -pix_fmt yuv420p cas1.mp4'
clean = 'ls *.png | while read n; do rm $n; done'


def ascii_art(n, N, rate):
    os.system('clear')
    colors = {0: '\033[31m',
              1: '\033[32m',
              2: '\033[33m',
              3: '\033[34m',
              4: '\033[36m',
              5: '\033[38m'}
    color = colors[np.random.random_integers(0,len(colors.keys())-1,1)[0]]
    print '\033[1m'+color+'='*70
    print ' _______                              ______                    ____'
    print '|__   __|    __     __        ___    | _____| _______  __   __ | ___|'
    print '   | |      /  \\   /  \\      / _ \\   | |  ___ |__  __||  \\  | || |_'
    print '   | |     /  _ \\_/ _  \\    / /_\ \\  | | |_  |   | |  |   \\ | ||  _|'
    print ' __| |__  /  / \\   / \\  \\  /  __   \\ | |___| | __| |_ |  |\\   || |__'
    print '|_______|/__/   \\_/   \\__\\/__/   \\__\\|_______||______||__| \\__||____|'
    print ''
    print ' [*] Mutation Rate: %s' % str(rate)
    print ' [*] %s Frames Simulated' % str(n)
    print '%s Percent Complete\t\t\t[%ss Elapsed]' % (str(100.*n/(N-1)), str(time.time()-tic))
    print '='*int(70.*n/N)+'\033[0m'


def fitness(chunk):
    rch = np.array(chunk[:, :, 0])
    gch = np.array(chunk[:, :, 1])
    bch = np.array(chunk[:, :, 2])
    fitness = rch.sum() + gch.sum() + bch.sum()
    if rch.sum() > R_THRESH:
        fitness -= (R_THRESH-rch.sum())
    if gch.sum() > G_THRESH:
        fitness -= (G_THRESH-gch.sum())
    if bch.sum() > B_THRESH:
        fitness -= (B_THRESH - bch.sum())
    return fitness


# Automatatize isnt working very well at all
def automatatize(world, ind2sub):
    rch = world[:, :, 0]
    gch = world[:, :, 1]
    bch = world[:, :, 2]

    rc1 = ndi.convolve(rch, k0, origin=0)
    gc1 = ndi.convolve(gch, k0, origin=0)
    bc1 = ndi.convolve(bch, k0, origin=0)

    # rc2 = ndi.convolve(rch, k1, origin=0)
    gc2 = ndi.convolve(gch, k1, origin=0)
    # bc2 = ndi.convolve(bch, k1, origin=0)

    for ii in range(world.shape[0]*world.shape[1]):
        [x, y] = ind2sub[ii]
        if not rc1 and rc1%4 == 0:
            world[x, y, 0] += 1
        if not gc1 and gc1 % 3 == 0:
            world[x, y, 1] += 1
        if not bc1 and bc1 % 4 == 0:
            world[x, y, 2] += 1
        if not bch[x, y] and not rch[x,y] and not gch[x,y]:  # black pixel
            if rc1[x, y] > 4:
                world[x, y, 0] = 1
        if gc1[ii] > 3 or gc2[ii] == 4:
            world[x - 1:x + 1, y - 1:y + 1, 1] = np.random.random_integers(0, mutation_rate, 8).reshape((2, 2))
        if rch[x,y] and gch[x,y] and bch[x,y]:  # White Pixel
            if gch[x,y] > gc1.mean() and gc1[ii] == 4:
                world[x - 1:x + 1, y - 1:y + 1, 0] = np.random.random_integers(0, mutation_rate, 8).reshape((2, 2))
        if gc1[ii]>2 and rc1[ii]:
            world[x,y,:] = 0
    return world


def simulation(world, depth, mutation_rate, save):
    print '[*] Simulation Started '
    f = plt.figure()
    reel = []
    reel.append([plt.imshow(world)])
    ind2sub = imutils.LIH_flat_map_creator(world[:, :, 0])
    for step in range(depth):
        ascii_art(step, depth, mutation_rate)
        weights = []
        world += np.random.random_integers(0,1,world.shape[0]*world.shape[1]*3).reshape((world.shape))
        for x in range(WIDTH):
            for y in range(HEIGHT):
                try:

                    mutation = np.random.random_integers(0, mutation_rate, 12).reshape((2, 2, 3))
                    block = world[x - 1:x + 1, y - 1:y + 1, :]
                    fit = fitness(block)
                    if fit < (R_THRESH + G_THRESH + B_THRESH):
                        world[x - 1:x + 1, y - 1:y + 1, :] = mutation
                    weights.append(fit)
                except:
                    pass
        world = automatatize(world, ind2sub)
        if save:
            misc.imsave('pic%d.png' % step, world)
        reel.append([plt.imshow(world)])

    print '[*] Simulation [%ss Elapsed]' % str(time.time()-tic)
    a = animation.ArtistAnimation(f, reel, interval=100, blit=True, repeat_delay=900)
    print '[*] Rendering Finished [%ss Elapsed]' % str(time.time()-tic)
    plt.show()


def dissolve(state, depth, save):
    f = plt.figure()
    film = []
    film.append([plt.imshow(state)])
    film.append([plt.imshow(state)])
    film.append([plt.imshow(state)])
    ind2sub = imutils.LIH_flat_map_creator(state[:, :, 0])

    ''' Pre-Process Image In '''
    state[:, :, 0] = state[:, :, 0] - state[:, :, 0].mean()
    state[:, :, 1] = state[:, :, 1] - state[:, :, 1].mean()
    state[:, :, 2] = state[:, :, 2] - state[:, :, 2].mean()
    for step in range(depth):
        ascii_art(step, depth, 0)
        rch = np.array(state[:, :, 0])
        gch = np.array(state[:, :, 1])
        bch = np.array(state[:, :, 2])

        rc1 = ndi.convolve(rch, k0, origin=0)
        gc1 = ndi.convolve(gch, k0, origin=0)
        bc1 = ndi.convolve(bch, k0, origin=0)

        rmean = rc1.mean()
        gmean = gc1.mean()
        bmean = bc1.mean()

        for ii in range(state.shape[0]*state.shape[1]):
            [x, y] = ind2sub[ii]
            if (not rch[x, y] and not gch[x, y] and not bch[x, y]) or (rc1[x,y]<rmean and gc1[x,y]<gmean and bc1[x,y]<bmean):   # Black Pixel
                if gch[x, y] % 4 ==0:
                    state[x, y, 2] += 1
                if rch[x, y] % 4 == 0:
                    state[x, y, 0] -= 1
                    state[x, y, 2] -= 1
            if not rc1[x,y]%6 and gch[x, y]> 1.2*gmean:
                state[x, y, 0] += 1
                state[x, y, 2] -= 1
            if rch[x, y] > 100 and gch[x,y] > 100 and bch[x, y] > 100:
                ind = np.random.random_integers(0,2,1)[0]
                state[x,y,ind] -= 1
                if rc1[x,y] % 6 and bc1[x,y] % 6 == 0:
                    state[x, y, 0] -= 1
                    state[x, y, 1] += 1
                    state[x, y, 2] -= 1
        # world = np.zeros(state.shape)
        state[:, :, 0] = rc1 - state[:, :, 0].mean()
        state[:, :, 1] = gc1 - state[:, :, 1].mean()
        state[:, :, 2] = bc1 - state[:, :, 2].mean()
        # film.append([plt.imshow(world - 2*state)])
        film.append([plt.imshow(state)])

    a = animation.ArtistAnimation(f, film, interval=100, blit=True, repeat_delay=900)
    print 'SIMILATION FINISHED [%ss Elapsed]' % str(time.time()-tic)
    if save:
        writer = animation.FFMpegWriter(fps=5,bitrate=1800)
        a.save('earth_gif.mp4', writer)
    plt.show()


def beatify(state, depth, save):
    f = plt.figure()
    film = []
    film.append([plt.imshow(state)])
    ind2sub = imutils.LIH_flat_map_creator(state[:, :, 0])

    ''' Pre-Process Image In '''
    state[:, :, 0] = state[:, :, 0] - state[:, :, 0].mean()
    state[:, :, 1] = state[:, :, 1] - state[:, :, 1].mean()
    state[:, :, 2] = state[:, :, 2] - state[:, :, 2].mean()
    for step in range(depth+1):
        ascii_art(step, depth, 0)
        rch = np.array(state[:, :, 0])
        gch = np.array(state[:, :, 1])
        bch = np.array(state[:, :, 2])

        rc1 = ndi.convolve(rch, k0, origin=0)
        gc1 = ndi.convolve(gch, k0, origin=0)
        bc1 = ndi.convolve(bch, k0, origin=0)

        rmean = rc1.mean()
        gmean = gc1.mean()
        bmean = bc1.mean()
        for ii in range(state.shape[0] * state.shape[1]):
            [x, y] = ind2sub[ii]
            if rc1[x,y] < rmean and gc1[x, y] < gmean and bc1[x, y] < bmean:
                state[x,y,0] += 1
            if gc1[x,y] < gmean and rc1[x, y] < rmean and bc1[x, y] < bmean:
                state[x,y,1] += 1
            if bc1[x,y] < bmean and rc1[x, y] < rmean and gc1[x, y] < gmean:
                state[x,y,2] += 1

            if rc1[x,y] > rmean and gc1[x, y] < gmean and bc1[x, y] < bmean:
                state[x,y,0] -= 1
            if gc1[x,y] > gmean and rc1[x, y] < rmean and bc1[x, y] < bmean:
                state[x,y,1] -= 1
            if bc1[x,y] > bmean and rc1[x, y] < rmean and gc1[x, y] < gmean:
                state[x,y,2] -= 1

        film.append([plt.imshow(state)])
    a = animation.ArtistAnimation(f, film, interval=100, blit=True, repeat_delay=900)
    print 'SIMILATION FINISHED [%ss Elapsed]' % str(time.time() - tic)
    if save:
        writer = animation.FFMpegWriter(fps=30, bitrate=1800)
        a.save('earth_gif.mp4', writer)
    plt.show()


if __name__ == '__main__':
    WIDTH = 60
    HEIGHT = 60
    DEPTH = 150
    save = True
    world = np.zeros((WIDTH, HEIGHT, 3))
    # SAPLING
    world[:, :, 1] = imutils.draw_centered_box(world[:, :, 1], 3, 15, False)
    if '-i' in sys.argv and len(sys.argv) == 3:
        world = np.array(plt.imread(sys.argv[2])).astype(np.int64)
        WIDTH = world.shape[0]
        HEIGHT = world.shape[1]
    mutation_rate = int((R_THRESH+G_THRESH+B_THRESH)/3)
    print '[*] Using Mutation Rate: %s' % str(mutation_rate)

    if '-test' in sys.argv:
        simulation(world, DEPTH, mutation_rate, save)
    if '-d' in sys.argv:
        dissolve(world, DEPTH, save)
    beatify(world, DEPTH, save)

    # if save:
    #     os.system(ani_cmd)
    #     os.system(clean)
