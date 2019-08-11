import matplotlib.pyplot as plt
import scipy.misc as misc
import numpy as np
import sys
import os


def create_board(width, height):
    bszx = int(np.ceil(width/8))
    bszy = int(np.ceil(height/8))

    ksq = np.zeros((bszx, bszy))
    wsq = np.ones((bszx, bszy))
    rowA = np.concatenate((wsq,ksq,wsq,ksq,wsq,ksq,wsq,ksq),0)
    rowB = np.concatenate((ksq,wsq,ksq,wsq,ksq,wsq,ksq,wsq),0)
    board = np.concatenate((rowA,rowB,rowA,rowB,rowA,rowB,rowA,rowB),1)
    plt.imshow(board, 'gray')
    plt.show()
    return board


if 'board' in sys.argv:
    chess_board = create_board(450, 450)
    misc.imsave('chess_board.png', chess_board)

