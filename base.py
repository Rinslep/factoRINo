# -*- coding: utf-8 -*-
"""
Useful Things - Temp(hopefully)
https://docs.python.org/3/library/functions.html#property
https://dbader.org/blog/python-dunder-methods
https://stackoverflow.com/questions/34273544/how-to-check-if-a-key-value-pair-is-present-in-a-dictionary
"""

"""
TODO:
    Go through dunder methods, understand and add to classes.
    Setup subclasses:
        Machines, modules_slots:
            if you know all of the possible values,
            then you can create a subclass.
            I know machine will either be a Furnace, Drill or Assembly
    Get to Green Circuits in crafting
    Print crafting Tree:
        print total of each resource
        +, -, *, /, ==, <
    modules, beacons
    maybe have seperate threads looking down different trees
    OR
    maybe have the data stored for low computation.
    have everything read from recipe file:
        currently works, but will break when you try to save
        items/machines that are not bound to a recipe are going be skipped
        this could be solved by calling it an init file or some other
        meaningful_variable_name
    
"""
#import pygame as p
#from functools import total_ordering # must use, v useful
import pickle
temp = "machines", "items"
filenames = ["recipes"]

class Machine(object): # Need machineType sub-classes
    machines_dict = {}
    def __init__(self, name:str, crafting_speed:float, module_slots:int):
        self.name = name
        self.crafting_speed = crafting_speed
        self.module_slots = module_slots
        
        if name not in Machine.machines_dict.keys():
            Machine.machines_dict[self.name] = self
    
        
    
        
class Furnace(Machine):
    def __repr__(self):
        return ("Furnace('{}',{},{})" .format(self.name, \
                                             self.crafting_speed, \
                                             self.module_slots))

class Drill(Machine):
    def __repr__(self):
        return ("Drill('{}',{},{})" .format(self.name, \
                                             self.crafting_speed, \
                                             self.module_slots))

class Assembly(Machine):
    def __repr__(self):
        return ("Assembly('{}',{},{})" .format(self.name, \
                                             self.crafting_speed, \
                                             self.module_slots))


class Item(object):
    items_dict = {}
    def __init__(self, name:str, machine_type:type):
        self.name = name
        self.machine_type = machine_type
        if name not in Item.items_dict.keys():
            Item.items_dict[self.name] = self
        
    def __repr__(self):
        return ("Item('{}', {})" .format(self.name, \
                                      self.machine_type))
        

class Basic_Item(Item):
    pass


class Recipe(object):
    recipes_dict = {}
    def __init__(self, machine_type:type, base_speed:float, \
                 output:list, input_:list):
        """
        output and inputs expects tuples of format (Item, quantity:int)
        """
        self.machine_type = machine_type
        self.base_speed = base_speed
        self.output = output
        self.input_ = input_
        name = output[0]
        
        if name not in Recipe.recipes_dict.keys():
            Recipe.recipes_dict[name] = self
    
    def __repr__(self):
        return ("Recipe({},{},{},{})" .format(self.machine_type, \
                                            self.base_speed, self.output, \
                                            self.input_))   


def pickle_write(filename:str, objects:list):
    with open("p_" + filename, "wb") as f:
        for obj in objects:
            pickle.dump(obj, f)

def pickle_read(filename:str):
    with open("p_" + filename, "rb") as f:
        pickle.load(f) # classes should add themselves to dict
        print("Read file: {}".format(filename))


def update_files():
    pickle_write("items", list(Item.items_dict.values()))
    pickle_write("machines", list(Machine.machines_dict.values()))
    pickle_write("recipes", list(Recipe.recipes_dict.values()))
    
def init_test_data(file_overwrite = True): 
    mining_drill = Drill("mining_drill", 0.5, 3) 
    stone_furnace = Furnace("stone_furnace", 1, 0)
    copper_ore = Item("copper_ore", Drill)
    copper_plate = Item("copper_plate", Furnace)
    copper_ore_to_plate = Recipe("furnace", "3.2", (copper_plate,1), \
                                 (copper_ore,1))
    
    if file_overwrite: update_files()

def read_or_write_data(should_init = False):
    init_test_data(should_init)
    if not should_init:
        for fn in filenames:
            pickle_read(fn)

read_or_write_data()

for item in Item.items_dict.items():
    print(item)

for machine in Machine.machines_dict.items():
    print(machine)
    
for recipe in Recipe.recipes_dict.items():
    print(recipe)


#p.init()
#
#display = p.display.set_mode((1024,768))
#p.display.set_caption("Factorio Base Planner")
#

#crashed = False
#while not crashed:

#    for event in p.event.get():
#        if event.type == p.QUIT:
#            crashed = True
     
    
        #print(event)  #Can be used to get event triggers

#    p.display.update()

#p.quit()
#quit()
