import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()
ani_cmd = 'ffmpeg -loglevel quiet -r 5 -i img%02d.png -vcodec libx264 -pix_fmt yuv420p '
clean = 'ls *.png | while read n; do rm $n; done'

k0 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
k1 = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
k2 = [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]]


def generate_primordial_stew(width, height, show):
    rstate = np.random.random_integers(0, 16, width * height).reshape((width, height))
    gstate = np.random.random_integers(0, 16, width * height).reshape((width, height))
    bstate = np.random.random_integers(0, 16, width * height).reshape((width, height))

    world = np.zeros((width, height, 3))
    world[:, :, 0] = rstate
    world[:, :, 1] = gstate
    world[:, :, 2] = bstate
    if show:
        plt.imshow(world)
        plt.show()
    return world


def evolution(world, depth, save):
    print '[*] Starting Simulation [%ss Elapsed]' % str(time.time()-tic)
    frames = []
    if save['show']:
        f = plt.figure()
    ind2sub = imutils.LIH_flat_map_creator(world[:,:,0])
    flipped = np.zeros((world.shape[0], world.shape[1]))
    for step in range(depth+1):
        rch = world[:, :, 0]
        gch = world[:, :, 1]
        bch = world[:, :, 2]

        rc0 = ndi.convolve(world[:, :, 0], k0, origin=0)
        gc0 = ndi.convolve(world[:, :, 1], k0, origin=0)
        bc0 = ndi.convolve(world[:, :, 2], k0, origin=0)

        rc1 = ndi.convolve(world[:, :, 0], k1, origin=0)
        gc1 = ndi.convolve(world[:, :, 1], k1, origin=0)
        bc1 = ndi.convolve(world[:, :, 2], k1, origin=0)

        rc2 = ndi.convolve(world[:, :, 0], k2, origin=0)
        gc2 = ndi.convolve(world[:, :, 1], k2, origin=0)
        bc2 = ndi.convolve(world[:, :, 2], k2, origin=0)
        fx = ndi.convolve(flipped, k2, origin=0)
        trigger = 3

        for ii in range(world.shape[0]*world.shape[1]):
            [x, y] = ind2sub[ii]
            if rch[x,y] and gch[x,y] and bch[x,y]:       # White Pixel
                if rc0[x, y] % 4 == 0 and gc2[x, y] % 2==0 and bc0[x,y] % 5 == 0:
                    world[x, y, 0] = 0
                    world[x, y, 1] += 1
                    world[x, y, 2] = 0
                    flipped[x, y] += 1
            if rch[x,y] and not gch[x,y] and not bch[x,y]:  # Red Pixel
                if rc2[x,y] % 4 == 0 and (gc2[x,y] and bc2[x,y]) <= 4:
                    world[x, y, 0] += 1
                    world[x, y, 1] = 0
                    world[x, y, 2] = 0
                    flipped[x, y] += 1
                if rc2[x,y] % 5 == 0:
                    world[x, y, 0] -= 1
                    world[x, y, 1] = 0
                    world[x, y, 2] += 1
                    flipped[x, y] = 0
            if bch[x, y] and rch[x, y] and not gch[x, y]:  # M
                if bc1[x, y] % 3 == 0 and gc1[x, y] % 2 == 0 and rc1[x,y] % 4 == 0:
                    world[x, y, 0] = 0
                    world[x, y, 1] += 1
                    world[x, y, 2] += 1
                    flipped[x, y] += 1
            if gch[x,y] and not rch[x,y] and not bch[x,y]:
                if gc0[x,y] % 3 and bc0[x,y]<4:
                    world[x, y, 0] = 0
                    world[x, y, 1] -= 1
                    world[x, y, 2] = 0
            if fx[x,y] > trigger:
                if (rc2[x, y] or gc2[x,y] or bc2[x,y]) > trigger:
                    world[x,y,:] -= 1
            if not rch[x, y] and not gch[x, y] and not bch[x, y]:   # Black pixel
                if rc2[x, y] >= 4 or rc0[x, y] % 4 == 0:
                    world[x, y, 0] += 1
                    world[x, y, 1] = 0
                    world[x, y, 2] = 0
                    flipped[x, y] = 0

        frames.append([plt.imshow(world)])
    print '%d Frame Simulation Finished. [%ss Elapsed]' % (len(frames), str(time.time()-tic))
    if save['show']:
        print 'Finished Rendering [%ss Elapsed]' % str(time.time()-tic)
        a = animation.ArtistAnimation(f, frames, interval=save['frame_rate'], blit=True, repeat_delay=900)
        writer = animation.FFMpegWriter(fps=save['frame_rate'],bitrate=1800)
        a.save(save['name'],writer)
        plt.show()


def dream(im1, im2, depth):
    print '\033[1m[*] Starting Simulation\033[0m'
    reel = []
    f = plt.figure()
    dx1 = im1.shape[0]
    dy1 = im1.shape[1]
    dx2 = im2.shape[0]
    dy2 = im2.shape[1]
    if dx1 >= dx2:
        dx = dx1
    else:
        dx = dx2
    if dy1 >= dy2:
        dy = dy1
    else:
        dy = dy2
    im = np.zeros((dx, dy))
    cx = int(dx/2)
    cy = int(dy/2)
    sx = int(im1.shape[0]/2)
    sy = int(im1.shape[1]/2)

    n1 = [[0,0,1,1,0,0],
          [0,1,1,1,1,0],
          [1,1,1,1,1,1],
          [1,1,1,1,1,1],
          [0,1,1,1,1,0],
          [0,0,1,1,0,0]]

    n2 = [[0, 5, 0], [1, -1, 1], [0, 5, 0]]

    im[cx-sx:cx+sx, cy-sy:cy+sy] = im1[:,:,2]
    state = im2[cx-sx:cx+sx, cy-sy:cy+sy, 2]
    ind2sub = imutils.LIH_flat_map_creator(im)
    flipped = np.zeros((dx, dy))
    for step in range(depth):
        spread1 = ndi.convolve(im1[:,:,0], n1, origin=0)
        spread2 = ndi.convolve(im2[:,:,0], n1, origin=0)
        for ii in range(dx*dy):
            flip = np.random.random_integers(0,255,1)[0]
            [x, y] = ind2sub[ii]
            try:
                box2 = im2[x-2:x+2, y-2:y+2]
                if (spread1[x, y] % 10 or spread1[x, y] % 7) == 0:
                    im[x, y] = 1
                    flipped[x, y] += 1
                if spread1[x,y] % 8==0:
                    im[x, y] -= 1
                    flipped[x,y] += 1
                if flip == 255 or flipped[x,y]>10:
                    im[x - 2:x + 2, y - 2:y + 2] = box2
                if im[x, y] == 0:
                    if im2[x-2:x+2, y-2:y+2].sum() == box2.sum():
                        im[x - 2:x + 2, y - 2:y + 2] = box2
            except IndexError:
                pass
            except ValueError:
                pass

        reel.append([plt.imshow(im, 'gray')])
    a = animation.ArtistAnimation(f, reel, interval=30, blit=True, repeat_delay=900)
    print '\033[1m[*] Simulation Finished [%ss Elapsed]\033[0m' % str(time.time()-tic)
    plt.show()


if __name__ == '__main__':
    date, localtime = imutils.create_timestamp()
    name_out = (imutils.arr2string(date)+'_'+imutils.arr2string(localtime)).replace(' ','').replace('/','').replace(':','')
    file_name = 'test_'+name_out+'_.mp4'

    if '-sim' in sys.argv:
        w = 100
        h = 100
        depth = 525
        opts = {'save': True,
                'show': True,
                'frame_rate': 50,
                'name': file_name}
        initial_state = generate_primordial_stew(w, h, show=False)

        evolution(initial_state, depth, opts)

    ''' Try to optimize an image that contains both'''
    if '-dream' in sys.argv:
        if len(sys.argv) >=4:
            im1 = np.array(plt.imread(sys.argv[2]))
            im2 = np.array(plt.imread(sys.argv[3]))
        else:
            im1 = np.array(plt.imread('cat.jpeg'))
            im2 = np.array(plt.imread('earth.jpeg'))
        dream(im1, im2, 80)
