from tkinter import *
from tkinter import ttk

root = Tk()


class custom(Frame):
    def __init__(self, *configs):
        super(custom, self, *configs).__init__()
        ttk.Button(self, text="Clicky!", command=test).grid()

    def make_label(self, txt):
        ttk.Label(self, text=txt).grid(column=1)


def test():
    print("Button Click")


c = custom()
d = custom()
c.grid(row=0)
d.grid(row=1)
c.make_label('Label')
root.mainloop()
