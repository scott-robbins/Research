import numpy as np


class particle:
    x = 0
    y = 0

    def __init__(self, inital_position):
        self.x = inital_position[0]
        self.y = inital_position[1]

    def update(self, xx, yy):
        self.x += xx
        self.y += yy

    def show(self):
        print '[%s, %s]' % (str(self.x), str(self.y))
