from source.Item import Item
import numpy as np

class Lane(object):
    def __init__(self, speed=0.03125, n_tiles=256,):
        self.speed = speed
        self.n_tiles = n_tiles

    @property
    def tps(self):
        return self.n_tiles * self.speed


class belt(Lane, Lane):
    def __init__(self, in_dir, out_dir, speed):
        pass
    