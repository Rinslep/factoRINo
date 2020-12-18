import tkinter as tk
from tkinter import ttk
from random import randint
import source.NodesAndConnections as NAC
from math import log2



root = tk.Tk()
root.title('factoRINo')

HEIGHT = 500
WIDTH = int(HEIGHT * (16 / 9))


def init_notebook(window):
    notebook = ttk.Notebook(window)
    notebook.pack(pady=15)
    return notebook


def notebook_add_frame(notebook, label):
    f = init_frame(notebook, label)
    notebook.add(f, text=label)
    return f


def init_canvas(frame):
    c = tk.Canvas(frame, height=HEIGHT, width=WIDTH, bg='#AAAAAA')
    c.pack(side=tk.LEFT)
    return c


def init_frame(window, frame_label):
    frame = tk.LabelFrame(window, text=frame_label, relief=tk.RIDGE)
    frame.grid(row=0, column=0)
    return frame


def init_NodesAndConnections(total_dict, notebook):
    frame = notebook_add_frame(notebook, '1')
    canvas = init_canvas(frame)

    def create_nodes(total_dict, canvas):
        d = {}
        t = sum(total_dict.values())

        for k, v in total_dict.items():
            c = randint(0, (WIDTH * HEIGHT))  # place randomly on the canvas
            d[k] = NAC.Node(canvas, c, log2(v) * 2, k, v)  # creates class and places it on the canvas, visible
        return d

    def create_lines(total_dict, canvas):
        tdk = iter(total_dict.keys())
        for item in tdk:
            for con_item in item.connected_items:
                try:
                    NAC.Connection(canvas, total_dict[item], total_dict[con_item])
                except NAC.ConnectionCreationError as e:
                    # print('Duplicate line - Not created')
                    pass
                except KeyError as e:
                    print('Not connected: ', e)

    d = create_nodes(total_dict, canvas)
    create_lines(d, canvas)

    for node in NAC.Node.nodes:
        node.raise_node()

    return frame, canvas


def init_machine_func(total_dict, notebook, timeframe=60):
    from source.Recipe import Recipe
    from source.Machine import Machine
    frame = notebook_add_frame(notebook, '2')
    for i, q in total_dict.items():
        r = Recipe.get_recipe(i)
        Machine.machines_needed(r, q, timeframe)
