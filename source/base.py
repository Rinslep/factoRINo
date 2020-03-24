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
    pass


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


class Recipe(object):
    recipes_dict = {}
    multi_crafting_list = []

    def __init__(self, time_in_seconds: float, output: tuple, inputs: tuple, name=None):
        """
        output and inputs expects a tuple of format (item:Item, quantity:int)
        """
        self.time = time_in_seconds
        self.output = output
        self.inputs = inputs
        if name is not None:
            self.name = name
        else:
            self.name = self.output[0]
        # for item in self.get_output_item():
        #     item.add_possible_recipe(self)
        if self.num_outputs == 1:
            self.output[0].add_possible_recipe(self)
        else:
            for item, quantity in self.output:
                item.add_possible_recipe(self)


        # if self.item in Recipe.recipes_dict.keys():
        #     if not self.inputs == Recipe.recipes_dict[self.item]:  # if not same recipe
        #         self.multi_crafting_list.append(self.item)  # add to list of items with multiple recipes
        #     else:
        #         self.item.add_possible_recipe(self)
        # else:
        #     Recipe.recipes_dict[self.item] = self  # classes should add themselves to recipes_dict with no duplicates
        #     self.item.add_possible_recipe(self)

    def __repr__(self):
        return "{}({},{},{})".format(type(self).__name__, self.time, self.output, self.inputs)

    @property
    def output_quantity(self):
        return self.output[1]

    @property
    def num_inputs(self):
        if not isinstance(self.inputs[0], tuple):
            return 1
        else:
            return len(self.inputs)

    @property
    def num_outputs(self):
        if not isinstance(self.output[0], tuple):
            return 1
        else:
            return len(self.output)

    @staticmethod
    def get_recipe_from_string(s: str):
        return Item.get_item_from_string(s).recipes[0]

    @staticmethod
    def get_recipe(item):
        """
        :param item: Item or String
        :return: Recipe of item
        """
        if isinstance(item, str):
            return Recipe.get_recipe_from_string(item)
        else:
            return item.get_recipe()

    @staticmethod
    def has_multi(input_item):
        if input_item in Recipe.multi_crafting_list:
            return True
        else: return False

    def get_ratio(self, input_item):
        if self.num_inputs == 1:
            if self.inputs[0] is input_item:
                return self.inputs[1] / self.output_quantity
        else:
            for item, quantity in self.inputs:
                if item is input_item:
                    return quantity / self.output_quantity

    def get_input_item(self):
        if self.num_inputs == 1:
            yield self.inputs[0]
            # yield StopIteration
        else:
            for input, quantity in self.inputs:
                yield input
            # yield StopIteration

    def get_output_item(self):
        if self.num_outputs == 1:
            return self.output[0]
            # yield StopIteration
        else:
            for output, quantity in self.output:
                yield output
            # yield StopIteration


class Item(object):
    items_dict = {}
    is_raw = False
    is_fluid = False


    def __init__(self, name: str, machine_type_crafted_in=Assembly):
        self.name = name
        self.crafted_in = machine_type_crafted_in
        self.recipes = []
        if self.name not in Item.items_dict.keys():
            Item.items_dict[self.name] = self

        if isinstance(self, Raw_Resource) or issubclass(type(self), Raw_Resource):
            self.is_raw = True

        if issubclass(type(self), Fluid_Handler):
            self.is_fluid = True

    def __repr__(self):
        return "{}('{}', {})".format(type(self).__name__, self.name, self.crafted_in)

    def add_possible_recipe(self, recipe):
        self.recipes.append(recipe)
        print(f"{self}: {recipe.name}")

    @property
    def has_multi(self):
        return len(self.recipes) > 1

    @staticmethod
    def get_item_from_string(s: str):
        return Item.items_dict[s]

    def get_recipe(self):
        return self.recipes[0]


class Raw_Resource(Item):
    """
    Any item that doesn't have an assembler Recipe should be here # maybe not?
    Examples would be copper/iron ore, oil, water etc.
    """


class Fluid_Item(Item, Fluid_Handler):
    pass


class Fluid_Raw_Resource(Raw_Resource, Fluid_Handler):
    pass


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
    m_mining_drill = Drill("mining_drill", 0.5, 3)
    m_stone_furnace = Furnace("stone_furnace", 1, 0)
    m_boiler = Fluid_Assembly("boiler", 1, 0)

    coal = Raw_Resource("coal", Drill)
    r_coal = Recipe(1, (coal, 1), (coal, 1))

    water = Fluid_Raw_Resource("water", Pump)
    f_r_water = Fluid_Recipe(1, (water, 1200), (water, 1200))

    steam = Fluid_Item("steam", Fluid_Assembly)
    f_r_steam = Fluid_Recipe(1, (steam, 60), (water, 60))

    crude_oil = Fluid_Raw_Resource("crude_oil", Pump)
    f_r_crude_oil = Fluid_Recipe(1, (crude_oil, 100), (crude_oil, 100))

    heavy_oil = Fluid_Item("heavy_oil", Fluid_Assembly)
    light_oil = Fluid_Item("light_oil", Fluid_Assembly)
    petroleum_gas = Fluid_Item("petroleum_gas", Fluid_Assembly)

    basic_oil = Fluid_Recipe(5, (petroleum_gas, 45), (crude_oil, 100), "basic_oil_processing")
    advanced_oil = Fluid_Recipe(5, ((heavy_oil, 25), (light_oil, 45), (petroleum_gas, 55)),
                                ((crude_oil, 100), (water, 50)), "advanced_oil_processing")
    coal_liquefaction = Fluid_Recipe(5, ((heavy_oil, 90), (light_oil, 20), (petroleum_gas, 10)),
                                     ((coal, 10), (heavy_oil, 25), (steam, 50)), "coal_liquefaction")

    heavy_cracking = Fluid_Recipe(2, (light_oil, 30), ((heavy_oil, 40), (water, 30)))
    light_cracking = Fluid_Recipe(2, (petroleum_gas, 20), ((light_oil, 30), (water, 30)))

    copper_ore = Raw_Resource("copper_ore", Drill)
    r_copper_ore = Recipe(1, (copper_ore, 1), (copper_ore, 1))

    copper_plate = Item("copper_plate", Furnace)
    r_copper_plate = Recipe(3.2, (copper_plate, 1), (copper_ore, 1))

    copper_cable = Item("copper_cable")
    r_copper_cable = Recipe(0.5, (copper_cable, 2), (copper_plate, 1))

    iron_ore = Raw_Resource("iron_ore", Drill)
    r_iron_ore = Recipe(1, (iron_ore, 1), (iron_ore, 1))

    iron_plate = Item("iron_plate", Furnace)
    r_iron_plate = Recipe(3.2, (iron_plate, 1), (iron_ore, 1))

    iron_gear_wheel = Item("iron_gear_wheel")
    r_iron_gear_wheel = Recipe(0.5, (iron_gear_wheel, 1), (iron_plate, 2))

    electronic_circuit = Item("electronic_circuit")
    r_electronic_circuit = Recipe(0.5, (electronic_circuit, 1), ((copper_cable, 3), (iron_plate, 1)))

    automation_science_pack = Item("automation_science_pack")
    r_automation_science_pack = Recipe(5, (automation_science_pack, 1), ((copper_plate, 1), (iron_gear_wheel, 1)))

    transport_belt = Item("transport_belt")
    r_transport_belt = Recipe(0.5, (transport_belt, 2), ((iron_gear_wheel, 1), (iron_plate, 1)))

    inserter = Item("inserter")
    r_inserter = Recipe(0.5, (inserter, 1), ((electronic_circuit, 1), (iron_gear_wheel, 1), (iron_plate, 1)))

    logistic_science_pack = Item("logistic_science_pack")
    r_logistic_science_pack = Recipe(6, (logistic_science_pack, 1), ((inserter, 1), (transport_belt, 1)))

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

    pipe = Item("pipe")
    r_pipe = Recipe(0.5, (pipe, 1), (iron_plate, 1))

    engine_unit = Item("engine_unit")
    r_engine_unit = Recipe(10, (engine_unit, 1), ((iron_gear_wheel, 1), (pipe, 2), (steel_plate, 1)))

    sulfur = Item("sulfur", Fluid_Assembly)
    f_r_sulfur = Fluid_Recipe(1, (sulfur, 2), ((petroleum_gas, 30), (water, 30)))

    plastic_bar = Item("plastic_bar", Fluid_Assembly)
    f_r_plastic_bar = Fluid_Recipe(1, (plastic_bar, 2), ((coal, 1), (petroleum_gas, 20)))

    advanced_circuit = Item("advanced_circuit")
    r_advanced_circuit = Recipe(6, (advanced_circuit, 1), ((copper_cable, 4), (electronic_circuit, 2),
                                                           (plastic_bar, 2)))

    chemical_science_pack = Item("chemical_science_pack")
    r_chemical_science_pack = Recipe(24, (chemical_science_pack, 2), ((advanced_circuit, 3), (engine_unit, 2),
                                                                      (sulfur, 1)))

    iron_stick = Item("iron_stick")
    r_iron_stick = Recipe(0.5, (iron_stick, 2), (iron_plate, 1))

    rail = Item("rail")
    r_rail = Recipe(0.5, (rail, 2), ((iron_stick, 1), (steel_plate, 1), (stone, 1)))

    productivity_module = Item("productivity_module")
    r_productivity_module = Recipe(15, (productivity_module, 1), ((advanced_circuit, 5), (electronic_circuit, 5)))

    m_electric_furnace = Furnace("electric_furnace", 2, 2)
    electric_furnace = Item("electric_furnace")
    r_electric_furnace = Recipe(5, (electric_furnace, 1), ((advanced_circuit, 5), (steel_plate, 10), (stone_brick, 10)))

    production_science_pack = Item("production_science_pack")
    r_production_science_pack = Recipe(21, (production_science_pack, 3), ((electric_furnace, 1),
                                                                          (productivity_module, 1), (rail, 30)))

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


def recipe_crawler(recipe: Recipe, total_dict=None, number_to_be_crafted=None, is_first_item=False) -> dict:
    """
    dictionary is edited in place
    """
    if total_dict is None:
        total_dict = {}
    if number_to_be_crafted is None:
        number_to_be_crafted = recipe.output_quantity

    if is_first_item:
        for output_item in recipe.get_output_item():
            add_to_dict(total_dict, output_item, number_to_be_crafted)  # can be added if total_dict is none

    for input_item in recipe.get_input_item():  # some form of generator
        modified_quantity = number_to_be_crafted * recipe.get_ratio(input_item)
        if not input_item.is_raw:  # if 1, non-raw or non-fluid, input.
            if input_item.has_multi:  # handles oil production or anything that has multiple recipes
                # do multi_crafting things
                print(f"multi: {input_item}")
            else:
                new_recipe = Recipe.get_recipe(input_item)
                add_to_dict(total_dict, input_item, modified_quantity)
                recipe_crawler(new_recipe, total_dict, modified_quantity)
        else:  # should handle raw resources like coal and ores
            add_to_dict(total_dict, input_item, modified_quantity)

    return total_dict


read_or_write_data()

r = Recipe.get_recipe("plastic_bar")

t_d = recipe_crawler(r, None, 3.0, True)

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