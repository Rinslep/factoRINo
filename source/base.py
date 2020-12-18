# -*- coding: utf-8 -*-
"""
Useful Things - Temp(hopefully)
https://docs.python.org/3/library/functions.html#property
https://dbader.org/blog/python-dunder-methods
"""

from source.data_getter import Data
import pickle
from source.Recipe import *
from source.Multi_Craft import *

"""
    have a recipe_group class/dict/namespace that can take n recipes
        can have recipes grouped together to make a collection of products
        in the same place. e.g. you want to make science in one place
            maybe be able to select what items get imported into the module
            and what gets produced on site. e.g. purple science...
                import iron plate and steel or make steel on site
    MAKE A DISPLAY
        needs to serve a purpose greater than just displaying data
            having an options menu to change a load of variables:
                modules, beacons, modded items/modules/beacons
            add new recipes, items or machines 
                all with their own custom variables
                    use type to produce custom classes?
                    are metaclasses useful here?
"""
# from functools import total_ordering # must use, v useful
filenames = ["recipes", "machines", "items"]

def pickle_write(filename: str, objects: list):
    with open("p_" + filename, "wb") as f:
        for obj in objects:
            pickle.dump(obj, f)


def pickle_read(filename: str):
    with open("p_" + filename, "rb") as f:
        print("Read file: {}".format(filename))
        pickle.load(f)


def update_files():
    pickle_write("items", list(Item.items_dict.values()))
    pickle_write("machines", list(Machine.machines_dict.values()))
    pickle_write("recipes", list(Recipe.recipes_list))


def init_data():
    d = Data(Data.get_latest_version())
    for ts in d.read_relevant_files():
        for dl in d.data_extender(ts):
            recipe_from_string(dl)


# def read_or_write_data(should_init=False):
#     init_data()
#     if not should_init:
#         for fn in filenames:
#             pickle_read(fn)


# def get_list_item_quantity(_list):
#     for item, quantity in _list:
#         yield Item.get_item_from_string(item), int(quantity)
#     return StopIteration

# read_or_write_data()


# total = 0
# for value in t_d.values():
#     total += value
# needs to be some form of log average
# scale = total / len(t_d)

init_data()

r = Recipe.get_recipe("production-science-pack")
t_d = recipe_crawler(r, None, float(1000), True)
Multi_Craft.build_matrix()
Multi_Craft.simplex()

import source.Display as display

root = display.root
notebook = display.init_notebook(root)
f,c = display.init_NodesAndConnections(t_d, notebook)


display.init_machine_func(t_d, notebook, 60)

# for i in t_d.items():
#     print(i)


root.mainloop()

