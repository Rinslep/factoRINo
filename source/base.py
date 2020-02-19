# -*- coding: utf-8 -*-
"""
Useful Things - Temp(hopefully)
https://docs.python.org/3/library/functions.html#property
https://dbader.org/blog/python-dunder-methods
https://stackoverflow.com/questions/34273544/how-to-check-if-a-key-value-pair-is-present-in-a-dictionary
https://kbroman.org/github_tutorial/pages/first_time.html
"""

"""
TODO:
    Go through dunder methods, understand and add to classes.
        maybe use add classes in either item or machine
            this may let me forgo any extraneous calculations and have a
            more simple idea of the process to calculate a crafting tree.
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


class Fluid_Handler(object):
    """
    This will be a parent class of anything that needs to handle fluids.
    Fluids wont be put in for a while, but this placeholder means I can structure the program better for the future.
    Will need to have a fluid dict and add it to update_files
    """
    handles_fluids = True


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

    def __init__(self, name: str, machine_type_crafted_in=Assembly):
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
    Examples would be copper/iron ore, oil, water etc.
    """
    is_raw = True


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
    def get_recipe_from_string(s: str):
        return Recipe.recipes_dict[Item.items_dict[s]]

    @staticmethod
    def get_recipe(item: [Item, str]):
        """
        :param item: Item or String
        :return: Recipe of item
        """
        if isinstance(item, str):
            return Recipe.get_recipe_from_string(item)
        else:
            return Recipe.recipes_dict[item]

    def get_ratio(self, input_item: Item):
        if self.num_inputs == 1:
            if self.inputs[0] is input_item:
                return self.inputs[1] / self.output_quantity
        else:
            for item, quantity in self.inputs:
                if item is input_item:
                    return quantity / self.output_quantity


class Fluid_Recipe(Recipe, Fluid_Handler):
    pass


def pickle_write(filename: str, objects: list):
    with open("p_" + filename, "wb") as f:
        for obj in objects:
            pickle.dump(obj, f)


def pickle_read(filename: str):
    with open("p_" + filename, "rb") as f:
        pickle.load(f)
        # print("Read file: {}".format(filename))


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

    iron_gear_wheel = Item("iron_gear_wheel", Assembly)
    r_iron_gear_wheel = Recipe(0.5, (iron_gear_wheel, 1), (iron_plate, 2))

    electronic_circuit = Item("electronic_circuit", Assembly)
    r_electronic_circuit = Recipe(0.5, (electronic_circuit, 1), ((copper_cable, 3), (iron_plate, 1)))

    automation_science_pack = Item("automation_science_pack", Assembly)
    r_automation_science_pack = Recipe(5, (automation_science_pack, 1), ((copper_plate, 1), (iron_gear_wheel, 1)))

    transport_belt = Item("transport_belt")
    r_transport_belt = Recipe(0.5, (transport_belt, 2), ((iron_gear_wheel, 1), (iron_plate, 1)))

    inserter = Item("inserter")
    r_inserter = Recipe(0.5, (inserter, 1), ((electronic_circuit, 1), (iron_gear_wheel, 1), (iron_plate, 1)))

    logistic_science_pack = Item("logistic_science_pack")
    r_logistic_science_pack = Recipe(6, (logistic_science_pack, 1), ((inserter, 1), (transport_belt, 1)))

    coal = Raw_Resource("coal", Drill)
    r_coal = Recipe(1, (coal, 1), (coal, 1))

    grenade = Item("grenade")
    r_grenade = Recipe(8, (grenade, 1), ((coal, 10), (iron_plate, 5)))

    firearm_magazine = Item("firearm_magazine")
    r_firearm_magazine = Recipe(1, (firearm_magazine, 1), (iron_plate, 4))

    steel_plate = Item("steel_plate", Furnace)
    r_steel_plate = Recipe(16, (steel_plate, 1), (iron_plate, 5))

    piercing_rounds_magazine = Item("piercing_rounds_magazine")
    r_piercing_rounds_magazine = Recipe(3, (piercing_rounds_magazine, 1), ((copper_plate, 5),
                                                                           (firearm_magazine, 1), (steel_plate, 1)))

    stone = Raw_Resource("stone", Drill)
    r_stone = Recipe(1, (stone, 1), (stone, 1))

    stone_brick = Item("stone_brick", Furnace)
    r_stone_brick = Recipe(3.2, (stone_brick, 1), (stone, 2))

    stone_wall = Item("stone_wall")
    r_stone_wall = Recipe(0.5, (stone_wall, 1), (stone_brick, 5))

    military_science_pack = Item("military_science_pack")
    r_military_science_pack = Recipe(10, (military_science_pack, 2), ((grenade, 1), (piercing_rounds_magazine, 1),
                                                                      (stone_wall, 2)))

    if file_overwrite: update_files()


def read_or_write_data(should_init=False):
    init_test_data(should_init)  # will be replaced with something to handle non-reciped items and machines
    if not should_init:
        for fn in filenames:
            pickle_read(fn)


def add_to_dict(dict_to_add_to, item: Item, quantity: int):
    if item not in dict_to_add_to.keys():
        dict_to_add_to[item] = quantity
    else:
        cur_quantity = dict_to_add_to[item]
        dict_to_add_to[item] = cur_quantity + quantity


def recipe_crawler(recipe: Recipe or str, total_dict=None, number_to_be_crafted=None, first_item=False) -> dict:
    """
    dictionary is edited in place
    """
    if total_dict is None:
        total_dict = {}
    if number_to_be_crafted is None:
        number_to_be_crafted = recipe.output_quantity

    output_item = recipe.output[0]
    if first_item: add_to_dict(total_dict, output_item, number_to_be_crafted)

    if recipe.num_inputs == 1:  # only has a single item,quantity tuple
        input_item = recipe.inputs[0]
        modified_quantity = number_to_be_crafted * recipe.get_ratio(input_item)
        if not input_item.is_raw:  # if 1, non-raw, input.
            new_recipe = Recipe.get_recipe(input_item)
            add_to_dict(total_dict, input_item, modified_quantity)
            recipe_crawler(new_recipe, total_dict, modified_quantity)
        else:
            add_to_dict(total_dict, input_item, modified_quantity)
    else:  # otherwise it will have multiple item,quantity tuples and i can loop through them
        for input_item, input_quantity in recipe.inputs:
            modified_quantity = number_to_be_crafted * recipe.get_ratio(input_item)
            if not input_item.is_raw:
                new_recipe = Recipe.get_recipe(input_item)
                add_to_dict(total_dict, input_item, modified_quantity)
                recipe_crawler(new_recipe, total_dict, modified_quantity)
            else:  # should only reach this on things like grenades/concrete
                # print("{}, WE HIT A GRENADE!\n\n".format(recipe.output[0]))
                add_to_dict(total_dict, input_item, modified_quantity)
    return total_dict


read_or_write_data()

r = Recipe.get_recipe("military_science_pack")

t_d = recipe_crawler(r, None, 1.0, True)

for item in t_d.items():
    print(item)


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
