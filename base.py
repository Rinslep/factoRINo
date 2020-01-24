# -*- coding: utf-8 -*-
"""
Useful Things - Temp(hopefully)
https://docs.python.org/3/library/functions.html#property
https://stackoverflow.com/questions/34273544/how-to-check-if-a-key-value-pair-is-present-in-a-dictionary
"""
#import pygame as p

class Item(object):
    items_dict = {}
    def __init__(self, name:str, machineType:str):
        self.name = name
        self.machineType = machineType
        if name not in Item.items_dict.keys():
            Item.items_dict[self.name] = self
        
    def __repr__(self):
        return ("Item('{}','{}')" .format(self.name, \
                                      self.machineType))
        
        
class Machine(object): # Need machineType sub-classes
    machines_dict = {}
    def __init__(self, name:str, craftingSpeed:float, \
                 machineType:str, moduleSlots:int):
        self.name = name
        self.craftingSpeed = craftingSpeed
        self.machineType = machineType
        self.moduleSlots = moduleSlots
        
        if name not in Machine.machines_dict.keys():
            Machine.machines_dict[self.name] = self
        
    def __repr__(self):
        return ("Machine('{}',{},'{}',{})" .format(self.name, \
                                             self.craftingSpeed, \
                                             self.machineType, \
                                             self.moduleSlots))

class M_Furnace(Machine):
    pass


class Recipe(object):
    recipes_dict = {}
    def __init__(self, machineType:str, baseSpeed:float, \
                 output:list, inputs:list):
        """
        output and inputs expects tuples of format (Item, quantity:int)
        """
        self.machineType = machineType
        self.baseSpeed = baseSpeed
        self.output = output
        self.inputs = inputs
        name = output[0]
        
        if name not in Recipe.recipes_dict.keys():
            Recipe.recipes_dict[name] = self
    
    def __repr__(self):
        return ("Recipe('{}',{},{},{})" .format(self.machineType, \
                                            self.baseSpeed, self.output, \
                                            self.inputs))   


def write_objects_to_file(filename:str, objects:list):  
    writeString = ""
    for obj in objects:
        writeString += repr(obj) + "\n"
    f = open(filename , "w+" )
    f.write(writeString)
    f.close()
    
def read_objects_from_file(filename:str):
    f = open(filename, "rt")
    for line in f.readlines():
        eval(line) #risky
    f.close()
    
def update_files():
#    print(list(Item.items_dict.values()))
    write_objects_to_file("items.txt", list(Item.items_dict.values()))
    write_objects_to_file("machines.txt", list(Machine.machines_dict.values()))
    write_objects_to_file("recipes.txt", list(Recipe.recipes_dict.values()))
    

mining_drill = Machine("mining_drill", 0.5, "drill", 3) 
stone_furnace = Machine("stone_furnace", 1, "furnace", 0)
copper_ore = Item("copper_ore", "drill")
copper_plate = Item("copper_plate", "furnace")

copper_ore_to_plate = Recipe("furnace", "3.2", (copper_plate,1), \
                                                 (copper_ore,1))


#write_objects_to_file("items.txt", w_items)
#write_objects_to_file("machines.txt", w_machines)

#read_objects_from_file("items.txt")
#read_objects_from_file("machines.txt")

for item in Item.items_dict.items():
    print(item)

for machine in Machine.machines_dict.items():
    print(machine)


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

update_files() # comment to prevent overriding of text files.
#p.quit()
#quit()
