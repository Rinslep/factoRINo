from tkinter import *
from random import randint, choice
from math import fmod
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
        self.create_node()

    def create_node(self):
        # print(self.image)
        a = Button(self.window, image=self.image, width=14, height=14, bg='#AAAAAA', activebackground='#AAAAAA', relief=FLAT)
        a.place(x=self.tl[0], y=self.tl[1])
        return a

    def reveal(self):
        a = self.window.itemconfigure('oval')
        print(a)

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

    @staticmethod
    def move(e):
        print(e)

    @classmethod
    def show_nodes(cls):
        for node in Node.nodes:
            node.reveal()


class Line(object):
    lines = []

    def __init__(self, a, b):
        self.a = a
        self.b = b

        Line.lines.append(self)

    @property
    def a_centre(self):
        return self.a.centre_coords

    @property
    def b_centre(self):
        return self.b.centre_coords

    @classmethod
    def draw_lines(cls, window):
        for line in Line.lines:
            window.create_line(line.a_centre, line.b_centre, fill='black', width=2)


root = Tk()
root.title('factoRINo')

HEIGHT = 500
WIDTH = int(HEIGHT * (16 / 9))

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='#AAAAAA')
canvas.pack(padx=50, pady=50, ipadx=10, ipady=10)
# create nodes
for i in range(20):
    c = randint(0, (WIDTH * HEIGHT))
    r = 10
    Node(canvas, c, r)

# create lines
for i in range(20):
    node_a = choice(list(Node.nodes))
    node_b = choice(list(Node.nodes))
    Line(node_a, node_b)

#https://stackoverflow.com/questions/49699802/understanding-tkinter-tag-bind

while __name__ == '__main__':
    canvas.delete(ALL)
    for node in Node.nodes:
        node.create_node()
    Line.draw_lines(canvas)
    root.mainloop()

