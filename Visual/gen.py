from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import imutils


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

width = 100
height = 100
state = np.zeros((width, height))
