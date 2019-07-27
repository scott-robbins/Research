import matplotlib.pyplot as plt
import scipy.misc as misc
import numpy as np
import imutils
import numpy
import time
import sys
import os

if '-circle' in sys.argv:
    try:
        size = int(sys.argv[2])
    except IndexError:
        print '** Incorrect Usage!! **'
        print 'ex: python imagen.py -circle 200'
        exit()
    circle = imutils.draw_centered_circle(np.zeros((2*size, 2*size)), size, 1, True)
    if '-save' in sys.argv and len(sys.argv) < 4:
        print '** Incorrect Usage!! **'
        print 'ex:'
        exit()
    elif '-save' in sys.argv and len(sys.argv) == 5:
        print 'Drawing Circle with radius %d and saving as %s' % (size, sys.argv[4])
        try:
            misc.imsave(sys.argv[4], circle)
        except ValueError:
            print '** Illegal File Extension! **'
            exit()
if '-box' in sys.argv:
    try:
        size = int(sys.argv[2])
    except IndexError:
        print '** Incorrect Usage!! **'
        print 'ex: python imagen.py -box 200'
        exit()
    box = imutils.draw_centered_box(np.zeros((2*size+10,2*size+10)), size, 1, True)
    if '-save' in sys.argv and len(sys.argv) < 4:
        print '** Incorrect Usage!! **'
        print 'ex:'
        exit()
    elif '-save' in sys.argv and len(sys.argv) == 5:
        print 'Drawing Box with radius %d and saving as %s' % (size, sys.argv[4])
        try:
            misc.imsave(sys.argv[4], box)
        except ValueError:
            print '** Illegal File Extension **'
            exit()

if '-red_box' in sys.argv:
    try:
        size = int(sys.argv[2])
    except IndexError:
        print '** Incorrect Usage!! **'
        print 'ex: python imagen.py -red_box 200'
        exit()
    box = imutils.draw_centered_box(np.zeros((2*size+10, 2*size+10, 3)), size, [1,0,0], True)
    if '-save' in sys.argv and len(sys.argv) < 4:
        print '** Incorrect Usage!! **'
        print 'ex:'
        exit()
    elif '-save' in sys.argv and len(sys.argv) == 5:
        print 'Drawing Box with radius %d and saving as %s' % (size, sys.argv[4])
        try:
            misc.imsave(sys.argv[4], box)
        except ValueError:
            print '** Illegal File Extension **'
            exit()

if '-green_box' in sys.argv:
    try:
        size = int(sys.argv[2])
    except IndexError:
        print '** Incorrect Usage!! **'
        print 'ex: python imagen.py -green_box 200'
        exit()
    box = imutils.draw_centered_box(np.zeros((2*size+10, 2*size+10, 3)), size, [0,1,0], True)
    if '-save' in sys.argv and len(sys.argv) < 4:
        print '** Incorrect Usage!! **'
        print 'ex:'
        exit()
    elif '-save' in sys.argv and len(sys.argv) == 5:
        print 'Drawing Box with radius %d and saving as %s' % (size, sys.argv[4])
        try:
            misc.imsave(sys.argv[4], box)
        except ValueError:
            print '** Illegal File Extension **'
            exit()

if '-blue_box' in sys.argv:
    try:
        size = int(sys.argv[2])
    except IndexError:
        print '** Incorrect Usage!! **'
        print 'ex: python imagen.py -blue_box 200'
        exit()
    box = imutils.draw_centered_box(np.zeros((2*size+10, 2*size+10, 3)), size, [0,0,1], True)
    if '-save' in sys.argv and len(sys.argv) < 4:
        print '** Incorrect Usage!! **'
        print 'ex:'
        exit()
    elif '-save' in sys.argv and len(sys.argv) == 5:
        print 'Drawing Box with radius %d and saving as %s' % (size, sys.argv[4])
        try:
            misc.imsave(sys.argv[4], box)
        except ValueError:
            print '** Illegal File Extension **'
            exit()

if '-ant' in sys.argv:
    state = np.zeros((175, 165,3))
    # Ant Body
    cx = state.shape[0]/2
    cy = state.shape[1]/2
    state[cy-50:cy+55, cx-55:cx+55] = [1,0,0]
    state[cy-20:cy+120,cx-75:cx+75] = imutils.draw_centered_circle(state[cy-20:cy+120,cx-75:cx+75], 57, [1,0,0], False)
    state[cy-80:cy,cx-75:cx+75,:] = imutils.draw_centered_circle(state[cy-80:cy,cx-75:cx+75],54,[1,0,0],False)
    ant = state[0:175,25:150,:]
    plt.imshow(ant)
    plt.show()
    if '-save' in sys.argv and len(sys.argv) < 4:
        print '** Incorrect Usage!! **'
        print 'ex:'
        exit()
    elif '-save' in sys.argv and len(sys.argv) == 4:
        print 'Drawing Ant and saving as %s' % ( sys.argv[3])
        try:
            misc.imsave(sys.argv[3], ant)
        except ValueError:
            print '** Illegal File Extension **'
            exit()
