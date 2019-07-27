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