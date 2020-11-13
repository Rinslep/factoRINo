from tkinter import *
from random import randint, choice
from math import fmod, dist, log10, sin, radians, degrees
from pathlib import Path


class Node(object):
    nodes = []
    image_folder = str(Path().absolute().parent / 'img')

    def __init__(self, window, centre, radius):
        self.window = window
        self.centre = centre  # single int, converted by the class to x, y
        self.radius = radius
        self.image = PhotoImage(file=self.image_folder+'/deault_circle.png')
        Node.nodes.append(self)
        self.oval_id = None
        self.create_oval_node()
        self.raise_node()
        self.lastx, self.lasty = self.tl
        self.connections = {}

    def create_oval_node(self):
        self.oval_id = self.window.create_oval(self.tl, self.br, fill='red')
        self.window.tag_bind(self.oval_id, '<Button-1>', lambda e: self.drag(e))
        self.window.tag_bind(self.oval_id, '<B1-Motion>', lambda e: self.drag(e), add='+')
        self.window.tag_bind(self.oval_id, '<Button-3>', lambda e: self.move(e), add='+')

    def move_centre(self, x, y):
        self.centre = self.coords_to_int(x, y, self.canvas_width)
        self.window.coords(self.oval_id, *self.tl, *self.br)
        self.move_connected_lines()

    @property
    def canvas_width(self):
        return int(self.window.cget('width'))

    @property
    def centre_coords(self):
        x = fmod(self.centre, self.canvas_width)
        y = (self.centre + 1) // self.canvas_width
        return int(x), int(y)

    @property
    def tl(self):
        tl = list(self.centre_coords)
        tl[0] = int(tl[0] - self.radius)
        tl[1] = int(tl[1] - self.radius)
        return tl

    @property
    def br(self):
        br = list(self.centre_coords)
        br[0] = int(br[0] + self.radius)
        br[1] = int(br[1] + self.radius)
        return br

    def add_connection(self, node, line):
        self.connections[node] = line

    def move(self, e):
        if any(self.connections):
            for node, line in self.connections.items():
                # print(f'n: {node}, L: {line}')
                d = line.length
                m = (self.radius * node.radius) / (d ** 2)
                a = log10(m * d)
                x1, y1, x2, y2 = line.dist_along(a)
                self.move_centre(x1, y1)
                node.move_centre(x2, y2)

    def drag(self, e):
        self.lastx, self.lasty = self.tl
        self.centre = (e.y * self.canvas_width) + e.x
        self.window.move(self.oval_id, self.tl[0] - self.lastx, self.tl[1] - self.lasty)
        self.lastx, self.lasty = self.tl
        self.move_connected_lines()
        self.raise_node()

    def move_connected_lines(self):
        for line in self.connections.values():
            line.move()

    def raise_node(self):
        self.window.tag_raise(self.oval_id)

    @classmethod
    def coords_to_int(cls, x, y, width):
        return int((y * width) + x)

    @classmethod
    def is_connected(cls, a, b):
        if b in a.connections.keys():
            raise LineExistsError


class Line(object):
    lines = []

    def __init__(self, window, a, b):
        self.window = window
        self.a = a
        self.b = b
        self.id = None
        self.create_line()
        Line.lines.append(self)
        a.add_connection(b, self)
        b.add_connection(a, self)

    @property
    def a_centre(self):
        return self.a.centre_coords

    @property
    def b_centre(self):
        return self.b.centre_coords

    @property
    def length(self):
        # could also minus both radius
        return dist(self.a_centre, self.b_centre)

    @property
    def line_slope(self):
        x1, y1 = self.a_centre
        x2, y2 = self.b_centre
        rise = y2 - y1
        run = x2 - x1
        return rise/run

    @property
    def canvas_width(self):
        return int(self.window.cget('width'))

    def get_direction(self):
        # a->b is opposite direction of b->a
        # down right is [True, True], up left is [False, False]
        return self.a_centre[0] > self.b_centre[0], self.a_centre[1] > self.b_centre[1]

    def dist_along(self, multiplier):
        d = (self.length * multiplier) / 2
        m = self.line_slope()
        c = self.a_centre[1] - (m * self.a_centre[0])


    def move(self):
        self.window.coords(self.id, *self.a_centre, *self.b_centre)

    def create_line(self):
        self.id = self.window.create_line(self.a_centre, self.b_centre, fill='black', width=2)


class LineExistsError(Exception):
    pass


root = Tk()
root.title('factoRINo')


HEIGHT = 500
WIDTH = int(HEIGHT * (16 / 9))

canvas = Canvas(root, height=HEIGHT, width=WIDTH, bg='#AAAAAA')
canvas.pack(padx=50, pady=50, ipadx=10, ipady=10, side=LEFT)
# create nodes
for i in range(30):
    c = randint(0, (WIDTH * HEIGHT))
    r = randint(10, 24)
    Node(canvas, c, r)

# create lines
for i in range(15):
    while True:
        try:
            node_a = choice(list(Node.nodes))
            node_b = choice(list(Node.nodes))
            while node_a is node_b:
                node_b = choice(list(Node.nodes))
            Node.is_connected(node_a, node_b)
            break
        except LineExistsError:
            pass
    # print(f'a:{node_a}, b:{node_b}')
    Line(canvas, node_a, node_b)

for node in Node.nodes:
    node.raise_node()

for line in Line.lines:
    print(f'a:{line.a_centre},{line.a.centre}:{Node.coords_to_int(*line.a_centre, line.canvas_width)}, b:{line.b_centre} = {line.length}')

while __name__ == '__main__':
    root.mainloop()

