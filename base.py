# -*- coding: utf-8 -*-
"""
Useful Things - Temp(hopefully)
https://docs.python.org/3/library/functions.html#property
https://dbader.org/blog/python-dunder-methods
https://stackoverflow.com/questions/34273544/how-to-check-if-a-key-value-pair-is-present-in-a-dictionary
https://kbroman.org/github_tutorial/pages/first_time.html
"""
import string

"""
TODO:
    Go through dunder methods, understand and add to classes.
        maybe use add classes in either item or machine
            this may let me forgo any extraneous calculations and have a
            more simple idea of the process to calculate a crafting tree.

    Print crafting Tree:
        print total of each resource
        +, -, *, /, ==, < (maybe not necessary)
    maybe have seperate threads looking down different trees
    OR (probably better to do at runtime)
    maybe have the data stored for low computation. 
    have everything read from recipe file:
        currently works, but will break when you try to save
        items/machines that are not bound to a recipe, which are going be 
        skipped. this could be solved by unpickling other_filenames
    have a recipe_group class/dict/namespace that can take n recipes
        can have recipes grouped together to make a collection of products
        in the same place. e.g. you want to make science in one place
            maybe be able to select what items get imported into the module
            and what gets produced on site. e.g. purple science...
                import iron plate and steel or make steel on site

    HANDLE FLUIDS LOL
        linear programming
            http://kirkmcdonald.github.io/posts/calculation.html
            fantastic explaination

    MAKE A DISPLAY
        needs to serve a purpose greater than just displaying data
            having an options menu to change a load of variables:
                modules, beacons
            add new recipes, items or machines 
                all with their own custom variables
                    use type to produce custom classes?
                    are metaclasses useful here?
"""

# import pygame as p
# from functools import total_ordering # must use, v useful
import pickle

other_filenames = "machines", "items"
filenames = ["recipes"]


class Fluid_Handler(object):
    """
    This will be a parent class of anything that needs to handle fluids.
    Fluids wont be put in for a while, but this placeholder means I can structure the program better for the future.
    Will need to have a fluid dict and add it to update_files
    """
    handles_fluids = True


class Recipe(object):
    recipes_dict = {}

    def __init__(self, time_in_seconds: float, output: tuple, inputs: tuple):
        """
        output and inputs expects a tuple of format (item:Item, quantity:int)
        """
        self.time = time_in_seconds
        self.output = output
        self.inputs = inputs

        if self.item not in Recipe.recipes_dict.keys():
            Recipe.recipes_dict[self.item] = self  # classes should add themselves to dict with no duplicates

    def __repr__(self):
        return "{}({},{},{})".format(type(self).__name__, self.time, self.output, self.inputs)

    @property
    def item(self):
        return self.output[0]

    @property
    def output_quantity(self):
        return self.output[1]

    @property
    def num_inputs(self):  # can be replaced with len? does it make sense to do so?
        if len(self.inputs) == 2 and not isinstance(self.inputs[0], tuple):
            return 1
        else:
            return len(self.inputs)

    @staticmethod
    def get_from_string(str):
        return Recipe.recipes_dict[Item.items_dict[str]]

    @staticmethod
    def get_recipe(item):
        if isinstance(item, str):
            return Recipe.get_from_string(item)
        else:
            return Recipe.recipes_dict[item]


class Fluid_Recipe(Recipe, Fluid_Handler):
    pass


class Machine(object):
    machines_dict = {}  # string:Machine

    def __init__(self, name: str, crafting_speed: float, module_slots: int):
        self.name = name
        self.crafting_speed = crafting_speed
        self.module_slots = module_slots

        if name not in Machine.machines_dict.keys():
            Machine.machines_dict[self.name] = self

    def __repr__(self):
        return "{}('{}',{},{})".format(type(self).__name__, self.name, self.crafting_speed, self.module_slots)


class Drill(Machine):
    # all but uranium
    pass


class Drill_Using_Fluid(Drill, Fluid_Handler):
    # used only for uranium mining
    pass


class Pump(Drill, Fluid_Handler):
    # oil and water
    pass


class Assembly(Machine):
    pass


class Fluid_Assembly(Assembly, Fluid_Handler):
    pass


class Furnace(Assembly):
    pass


class Item(object):
    items_dict = {}
    is_raw = False

    def __init__(self, name: str, machine_type_crafted_in: Machine):
        self.name = name
        self.crafted_in = machine_type_crafted_in

        if self.name not in Item.items_dict.keys():
            Item.items_dict[self.name] = self

        # if isinstance(self.crafted_in, Drill): self.is_raw = True

    def __repr__(self):
        return "{}('{}', {})".format(type(self).__name__, self.name, self.crafted_in)


class Raw_Resource(Item):
    """
    Any item that doesn't have an assembler Recipe should be here
    Examples would be copper ore, oil, water etc.
    """
    is_raw = True


def pickle_write(filename: str, objects: list):
    with open("p_" + filename, "wb") as f:
        for obj in objects:
            pickle.dump(obj, f)


def pickle_read(filename: str):
    with open("p_" + filename, "rb") as f:
        pickle.load(f)
        print("Read file: {}".format(filename))


def update_files():
    pickle_write("items", list(Item.items_dict.values()))
    pickle_write("machines", list(Machine.machines_dict.values()))
    pickle_write("recipes", list(Recipe.recipes_dict.values()))


def init_test_data(file_overwrite=False):
    mining_drill = Drill("mining_drill", 0.5, 3)
    stone_furnace = Furnace("stone_furnace", 1, 0)

    copper_ore = Raw_Resource("copper_ore", Drill)
    r_copper_ore = Recipe(1, (copper_ore, 1), (copper_ore, 1))

    copper_plate = Item("copper_plate", Furnace)
    r_copper_plate = Recipe(3.2, (copper_plate, 1), (copper_ore, 1))

    copper_cable = Item("copper_cable", Assembly)
    r_copper_cable = Recipe(0.5, (copper_cable, 2), (copper_plate, 1))

    iron_ore = Raw_Resource("iron_ore", Drill)
    r_iron_ore = Recipe(1, (iron_ore, 1), (iron_ore, 1))

    iron_plate = Item("iron_plate", Furnace)
    r_iron_plate = Recipe(3.2, (iron_plate, 1), (iron_ore, 1))

    electronic_circuit = Item("electronic_circuit", Assembly)
    r_electronic_circuit = Recipe(0.5, (electronic_circuit, 1), ((copper_cable, 3), (iron_plate, 1)))

    if file_overwrite: update_files()


def read_or_write_data(should_init=False):
    init_test_data(should_init)  # will be replaced with something to handle non-reciped items and machines
    if not should_init:
        for fn in filenames:
            pickle_read(fn)


read_or_write_data()


def add_to_dict(total_dict, item : Item, quantity: int):
    if item not in total_dict.keys():
        total_dict[item] = quantity
    else:
        cur_quantity = total_dict[item]
        total_dict[item] = cur_quantity + quantity


def recipe_crawler(recipe: Recipe or str, total_dict=None):
    """
    Currently displays full tree, but quantities are wrong.
    Need to take quantity needed for parent / quantity produced by child and multiply output by that amount
    """
    if total_dict is None:
        total_dict = {}

    print(recipe.inputs)
    if recipe.num_inputs == 1:  # only has a single item,quantity tuple
        print(recipe.inputs[1])
        add_to_dict(total_dict, *recipe.inputs)
        if not recipe.inputs[0].is_raw:  # if len 1 and not raw. basically 1 to 1 crafting like in furnace
            recipe_crawler(Recipe.get_recipe(recipe.inputs[0]), total_dict)
    else:  # otherwise it will have multiple item,quantity tuples and i can loop through
        for item, quantity in recipe.inputs:
            add_to_dict(total_dict, item, quantity)
            recipe_crawler(Recipe.get_recipe(item), total_dict)
    return total_dict


recipe = Recipe.get_recipe("electronic_circuit")

total_dict = {}
for i in range(1):
    total_dict.update(recipe_crawler(recipe, total_dict))

print("total_dict = ", total_dict)


# for item in Item.items_dict.values():
#     print(item)
#
# for machine in Machine.machines_dict.values():
#     print(machine)
#
# for recipe in Recipe.recipes_dict.values():
#    print(recipe)


# p.init()
#
# display = p.display.set_mode((1024,768))
# p.display.set_caption("Factorio Base Planner")
#

# crashed = False
# while not crashed:

#    for event in p.event.get():
#        if event.type == p.QUIT:
#            crashed = True

# print(event)  # Can be used to get event triggers

#    p.display.update()

# p.quit()

# quit()
