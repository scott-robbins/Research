from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from tqdm import tqdm
import numpy as np
import cauldron
import imutils
import time
import sys

known_colors = {'r': [1, 0, 0], 'g': [0, 1, 0], 'b': [0, 0, 1],
                'c': [0, 1, 1], 'm': [1, 0, 1], 'y': [1, 1, 0]}


def create_stew(s, pts, n):
    particles = []
    # Draw The initial points
    for color in pts.keys():
        for pt in pts[color]:
            [x, y] = pt
            point = cauldron.Particle([x, y], color, n)
            s[x, y, :] = known_colors[color]
            particles.append(point)
    # Add energy to the particles (random movements)
    for p in particles:
        p.steps = imutils.spawn_random_walk([p.x, p.y], n)
    return s, particles


def run_simulation(s, pts, n):
    k = [[1,1,1],[1,0,1],[1,1,1]]
    # k = np.ones((12, 12))
    f = plt.figure()
    progress = tqdm(total=n, unit=' generations')
    simulation.append([plt.imshow(s)])
    ''' Debug Variables '''
    flip_white = 0
    flip_yellow = 0
    '''       RUN SIMULATION      '''
    for step in range(n):
        rch = ndi.convolve(state[:,:,0],k,origin=0)
        gch = ndi.convolve(state[:,:,1],k,origin=0)
        bch = ndi.convolve(state[:,:,2],k,origin=0)
        for pt in pts:
            [x1, y1] = pt.steps[step]
            if step > 0:
                [x0, y0] = pt.steps[step - 1]
                try:
                    state[x0, y0, :] = 0
                except IndexError:
                    pass
            try:
                '''     Apply simulation rules here     '''
                # Rule Set 1
                if (rch[x1,y1] or gch[x1,y1] or bch[x1,y1]) >= 4:
                    pt.color = [1,1,1]
                    flip_white += 1
                if state[x1,y1,1] == 1 and gch[x1,y1] % 3:
                    pt.color = [1,1,0]
                    flip_yellow += 1

                # Rule Set 2 - Simple Virus
                # if (state[x1,y1,0] and state[x1,y1,1])==0 and state[x1, y1,2]==1 and rch[x1,y1]>0:
                #     pt.color = [1,0,0]
                # # Set the particle Color
                # state[x1, y1, :] = pt.color


            except IndexError:
                pass
        simulation.append([plt.imshow(s)])
        progress.update(1)
    progress.close()
    # print 'Yellow: %d' % flip_yellow
    # print 'White: %d' % flip_white
    a = animation.ArtistAnimation(f, simulation, interval=70, blit=True, repeat_delay=900)
    # if raw_input('Want to save (y/n)?').upper()=='Y':
    #     w = FFMpegWriter(fps=50, bitrate=3600)
    #     a.save('virus_sim_1.mp4', writer=w)
    plt.show()



if __name__ == '__main__':
    w = 250
    h = 250
    state = np.zeros((w, h, 3))
    k0 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

    '''
    Add Pockets of various colored particles
    and let them wander around
    '''
    # Add Initial Particles
    simulation = []
    n_total = 1000
    timesteps = 500

    # Create points for a simulation of evenly mixed points
    # stew, points = cauldron.add_even_particle_mix(state, n_total, ['r', 'b', 'g'])

    # Or use a Custom Configuration of Points
    stew, points = cauldron.add_custom_particle_mix(state, {'b': 750})
    points['r'].append([125, 125])
    points['r'].append([130, 115])
    points['r'].append([135, 105])

    # Give The points random steps
    state, particles = create_stew(state, points, timesteps)

    # Run it
    run_simulation(state, particles, timesteps)

