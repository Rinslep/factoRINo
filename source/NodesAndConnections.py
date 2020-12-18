import tkinter as tk
from math import fmod, dist, ceil
from pathlib import Path
from source.Item import Item


class Node(object):
    nodes = []
    image_folder = str(Path().absolute().parent / 'img')

    def __init__(self, window: tk.Canvas, center: int, radius: int, item: Item, value: float) -> object:
        self.window = window
        self.center = center  # single int, converted by the class to x, y
        self.radius = radius
        self.item = item
        self.value = value
        # try:
        #     self.image = tk.PhotoImage(file=self.image_folder + f'\{self.item.name.replace("-","_")}.png')
        # except tk.TclError:
        #     self.image = tk.PhotoImage(file=self.image_folder + '\default_circle.png')
        Node.nodes.append(self)
        self.node_id = None
        self.create_node('square')
        self.raise_node()
        self.lastx, self.lasty = self.tl
        self.connections = {}
        self.info = None
        self.info_last_pos = None

    @staticmethod
    def create_oval_node(parent, fill='red'):
        parent.node_id = parent.window.create_oval(parent.tl, parent.br, fill=fill)
        parent.window.tag_bind(parent.node_id, '<Button-1>', lambda e: parent.drag(e))
        parent.window.tag_bind(parent.node_id, '<B1-Motion>', lambda e: parent.drag(e), add='+')
        # self.window.tag_bind(self.oval_id, '<Button-3>', lambda e: self.move(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-2>', lambda e: parent.log(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-3>', lambda e: parent.display_info(e), add='+')

    @staticmethod
    def create_square_node(parent, fill='red'):
        parent.node_id = parent.window.create_polygon(parent.bbox, fill=fill)
        parent.window.tag_bind(parent.node_id, '<Button-1>', lambda e: parent.drag(e))
        parent.window.tag_bind(parent.node_id, '<B1-Motion>', lambda e: parent.drag(e), add='+')
        # self.window.tag_bind(self.oval_id, '<Button-3>', lambda e: self.move(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-2>', lambda e: parent.log(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-3>', lambda e: parent.display_info(e), add='+')

    def move_center(self, x, y):
        self.center = self.coords_to_int(x, y, self.canvas_width)
        self.window.coords(self.node_id, *self.tl, *self.br)
        self.move_connected_lines()

    @property
    def canvas_width(self):
        return int(self.window.cget('width'))

    @property
    def center_coords(self):
        x = fmod(self.center, self.canvas_width)
        y = (self.center + 1) // self.canvas_width
        return int(x), int(y)

    @property
    def tl(self):
        tl = list(self.center_coords)
        tl[0] = int(tl[0] - self.radius)
        tl[1] = int(tl[1] - self.radius)
        return tl

    @property
    def bl(self):
        bl = list(self.center_coords)
        bl[0] = int(bl[0] - self.radius)
        bl[1] = int(bl[1] + self.radius)
        return bl

    @property
    def br(self):
        br = list(self.center_coords)
        br[0] = int(br[0] + self.radius)
        br[1] = int(br[1] + self.radius)
        return br

    @property
    def tr(self):
        tr = list(self.center_coords)
        tr[0] = int(tr[0] + self.radius)
        tr[1] = int(tr[1] - self.radius)
        return tr

    @property
    def bbox(self):
        return self.tl, self.bl, self.br, self.tr

    def add_connection(self, node, line):
        self.connections[node] = line

    def move(self, e):
        # todo fix this - should move the node and its connections slightly closer together
        if any(self.connections):
            for node, line in self.connections.items():
                # print(f'n: {node}, L: {line}')
                x1, y1 = self.center_coords
                x2, y2 = node.center_coords
                p = x1, y2
                d = ceil(0.01 * line.length)

                self.move_center(x1, y1)
                node.move_center(x2, y2)

    def log(self, e):
        print(self.item, self.value)

    def drag(self, e):
        self.lastx, self.lasty = self.tl
        self.center = (e.y * self.canvas_width) + e.x
        self.window.move(self.node_id, self.tl[0] - self.lastx, self.tl[1] - self.lasty)
        self.lastx, self.lasty = self.tl
        self.move_connected_lines()
        self.hide_info()
        # self.raise_node()

    def move_connected_lines(self):
        for line in self.connections.values():
            line.move()

    def raise_node(self):
        self.window.tag_raise(self.node_id)

    @classmethod
    def coords_to_int(cls, x, y, width):
        return int((y * width) + x)

    @classmethod
    def is_connected(cls, a, b):
        if b in a.connections.keys():
            raise ConnectionCreationError

    @property
    def info_bbox(self):
        size = 60
        tl = [self.br[0], self.center_coords[1]]
        tr = [tl[0] + size, tl[1]]
        bl = [tl[0], tl[1] + size]
        br = [tl[0] + size, tl[1] + size]
        points = [tl, bl, br, tr]
        return points

    def move_info(self):
        x = self.info_bbox[0][0] - self.info_last_pos[0][0]
        y = self.info_bbox[0][1] - self.info_last_pos[0][1]
        self.window.moveto(self.info, x, y)
        self.info_last_pos = self.info_bbox

    def display_info(self, e):
        # self.info = None # todo replace this with logic to move the info box
        if self.info is None or self.info_last_pos is None:
            self.info_last_pos = self.info_bbox
            c = self.window.create_polygon(self.info_bbox, fill='#FF66F2', state=tk.NORMAL)
            self.info = c
            self.window.tag_bind(self.info, '<Button-2>', lambda e: self.log(e))
            return True
        if self.info_last_pos != self.info_bbox:
            self.move_info()
        self.window.itemconfigure(self.info, state=tk.NORMAL)

    def hide_info(self):
        self.window.itemconfigure(self.info, state=tk.HIDDEN)

    def create_node(self, shape):
        shapes = {'oval' : lambda x: Node.create_oval_node(x),
                  'square': lambda x: Node.create_square_node(x)}
        return shapes[shape](self)


class Connection(object):
    lines = []

    def __init__(self, window, a, b):
        try:
            Connection.check_exists(a, b)
        finally:
            self.window = window
            self.a = a
            self.b = b
            self.id = None
            self.create_line()
            Connection.lines.append(self)
            a.add_connection(b, self)
            b.add_connection(a, self)

    @property
    def a_center(self):
        return self.a.center_coords

    @property
    def b_center(self):
        return self.b.center_coords

    @property
    def length(self):
        # could also minus both radius
        return dist(self.a_center, self.b_center)

    @property
    def canvas_width(self):
        return int(self.window.cget('width'))

    # @property
    # def line_slope(self):
    #     x1, y1 = self.a_center
    #     x2, y2 = self.b_center
    #     rise = y2 - y1
    #     run = x2 - x1
    #     return rise/run

    # def get_direction(self):
    #     # a->b is opposite direction of b->a
    #     # down right is [True, True], up left is [False, False]
    #     return self.a_center[0] > self.b_center[0], self.a_center[1] > self.b_center[1]

    # def dist_along(self, multiplier):
    #     d = (self.length * multiplier) / 2

    def move(self):
        self.window.coords(self.id, *self.a_center, *self.b_center)

    def create_line(self):
        self.id = self.window.create_line(self.a_center, self.b_center, fill='black', width=2)

    @staticmethod
    def check_exists(a, b):
        if a == b:
            raise ConnectionCreationError
        for line in Connection.lines:
            nodes = [line.a, line.b]
            if a in nodes and b in nodes:
                raise ConnectionCreationError


class ConnectionCreationError(Exception):
    pass
