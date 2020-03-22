from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys
import os


def select_points(m):
    starts = []
    stops = []
    xx = 0
    for e2 in m[:, 0]:
        if e2 == 0:
            starts.append([xx, 0])
        xx += 1
    xx = 0
    for e2 in m[:, m.shape[1]-1]:
        if e2 == 0:
            starts.append([xx, m.shape[1]-1])
        xx += 1
    xx2 = 0
    for e3 in m[0, :]:
        if e3 == 0:
            stops.append([0, xx2])
        xx2 += 1

    start = starts.pop(np.random.random_integers(0, len(starts) - 1, 1)[0])
    stop = stops.pop(np.random.random_integers(0, len(stops) - 1, 1)[0])
    return start, stop


def check_solved(a, b):
    if a[0]==b[0] and a[1]==b[1]:
        print '\033[1m\033[32m[!!] SOLVED [!!]\033[0m'
        return True
    else:
        return False


def test_walk(im, a, b):
    f = plt.figure()
    solved = False
    test_ani = []
    test_ani.append([plt.imshow(im)])

    # Initialize position
    pos = a

    # Now Run The Walk
    while not solved and len(test_ani):
        directions = {1: [pos[0] - 1, pos[1] - 1],
                      2: [pos[0] - 1, pos[1]],
                      3: [pos[0] - 1, pos[1] + 1],
                      4: [pos[0], pos[1] - 1],
                      5: [pos[0], pos[1]],
                      6: [pos[0], pos[1] + 1],
                      7: [pos[0] + 1, pos[1] - 1],
                      8: [pos[0] + 1, pos[1]],
                      9: [pos[0] + 1, pos[1] + 1]}
        choices = []
        moves = {}
        for opt in directions.keys():
            [xi, yi] = directions[opt]
            try:
                if im[xi, yi, 0] == 1 and im[xi, yi, 1] == 1 and im[xi, yi, 2] == 1:
                    r = np.sqrt((xi ** 2 - b[0] ** 2) + (yi ** 2 - b[1] ** 2))
                    choices.append(r)
                    moves[r] = [xi, yi]
            except IndexError:
                continue
        try:
            best = np.array(choices).min()
        except ValueError:
            print '[!!] No Legal Moves Left'
            break
        if best not in moves.keys():
            try:
                best = choices.pop(0)
            except IndexError:
                print '[!!] No Legal Moves Left'
                break

        best_choice = moves[best]
        x = best_choice[0]
        y = best_choice[1]
        pos[0] = x
        pos[1] = y
        state[x,y,:] = [1,0,0]
        test_ani.append([plt.imshow(im)])
        solved = check_solved(pos,b)
    a = animation.ArtistAnimation(f,test_ani,interval=200,blit=True,repeat_delay=900)
    if raw_input('Save? [y/n]:').upper()=='y':
        w = FFMpegWriter(fps=10,bitrate=1800)
        name = raw_input('Enter File Name:')
        a.save(name, writer=w)
    plt.show()


def solver_one(im, a, b):
    f = plt.figure()
    solved = False
    ani = []
    ani.append([plt.imshow(im)])
    # Initialize
    pos = a
    k = [[1,1,1],[1,0,1],[1,1,1]]
    cutoff = 2750
    # Run The Simulation
    while not solved and len(ani) < cutoff:
        solved = check_solved(pos, b)
        directions = {1: [pos[0] - 1, pos[1] - 1],
                      2: [pos[0] - 1, pos[1]],
                      3: [pos[0] - 1, pos[1] + 1],
                      4: [pos[0], pos[1] - 1],
                      5: [pos[0], pos[1]],
                      6: [pos[0], pos[1] + 1],
                      7: [pos[0] + 1, pos[1] - 1],
                      8: [pos[0] + 1, pos[1]],
                      9: [pos[0] + 1, pos[1] + 1]}
        choices = []
        moves = {}
        world = ndi.convolve(im[:, :, 0],k,origin=0)
        for opt in directions.keys():
            [xi, yi] = directions[opt]
            try:
                if (state[xi,yi,0] and state[xi,yi,1] and state[xi,yi,2])==1:
                    if 1 <= world[xi,yi] <= 7:
                        r = np.sqrt((xi**2 - b[0]**2) + (yi**2 - b[1]**2))
                        if r == 0:
                            pos[0] = x
                            pos[1] = y
                            solved = True
                            print '\033[1m\033[32m[!!] SOLVED [!!]\033[0m'
                            continue
                        moves[r] = [xi, yi]
                        choices.append(r)
            except IndexError:
                continue
        try:
            best = np.array(choices).min()
        except ValueError:
            print '[!!] No Legal Moves Left'
            pass
        if best not in moves.keys():
            try:
                best = choices.pop()
            except IndexError:
                print '[!!] No Legal Moves Left'
                break

        best_choice = moves[best]
        x = best_choice[0]
        y = best_choice[1]
        pos[0] = x
        pos[1] = y
        state[x, y, :] = [1, 0, 0]
        ani.append([plt.imshow(im)])
    a = animation.ArtistAnimation(f,ani,interval=50,blit=True,repeat_delay=900)
    if raw_input('Do you want to save (y/n)?').upper()==('Y' or 'YES'):
        w = FFMpegWriter(fps=10, bitrate=1800)
        name = raw_input('Enter File Name:')
        a.save(name, writer=w)
    plt.show()


if __name__ == '__main__':
    maze_img = np.array(plt.imread('maze.png'))
    if len(maze_img.shape) == 2:
        state = np.zeros((maze_img.shape[0], maze_img.shape[1], 3))
        state[:, :, 0] = maze_img
        state[:, :, 1] = maze_img
        state[:, :, 2] = maze_img
    elif len(maze_img.shape) == 3:
        state = maze_img

    start, stop = select_points(maze_img)
    state = np.zeros((maze_img.shape[0], maze_img.shape[1], 3))
    state[:, :, 0] = maze_img
    state[:, :, 1] = maze_img
    state[:, :, 2] = maze_img
    # state[start[0]-1:start[0]+1, start[1]-1:start[1]+1, :] = [1, 0, 0]
    state[stop[0]-1:stop[0]+1, stop[1]-2:stop[1]+1, :] = [0, 1, 0]
    print 'Starting At: %s' % str(start)
    print 'Stopping At: %s' % str(stop)

    if'start' in sys.argv and len(sys.argv) >=4:
        start[0] = int(sys.argv[2])
        start[1] = int(sys.argv[3])

    stop = [0, 240]
    # test_walk(state, start, stop)
    solver_one(state, start, stop)
