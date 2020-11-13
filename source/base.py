# -*- coding: utf-8 -*-
"""
Useful Things - Temp(hopefully)
https://docs.python.org/3/library/functions.html#property
https://dbader.org/blog/python-dunder-methods
"""
from source.data_getter import Data

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

# import pygame as pyg
import pickle
import numpy as np

# from functools import total_ordering # must use, v useful
filenames = ["recipes", "machines", "items"]


def add_to_dict(dict_to_add_to, item, quantity: float):
    if item not in dict_to_add_to.keys():
        dict_to_add_to[item] = quantity
    else:
        cur_quantity = dict_to_add_to[item]
        dict_to_add_to[item] = cur_quantity + quantity


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


class Liquid(object):
    def __init__(self, name):

        pass


class Drill(Machine):
    # all but uranium
    pass


class Drill_Using_Fluid(Drill, Liquid):
    # used only for uranium mining
    pass


class Pump(Drill, Liquid):
    # oil and water
    pass


class Assembly(Machine):
    pass


class Fluid_Assembly(Assembly, Liquid):
    pass

class Rocket_Assembly(Assembly):
    pass

class Furnace(Assembly):
    pass


class Recipe(object):
    recipes_list = []
    categories = {'rocket-building': Rocket_Assembly,
                  'crafting': Assembly,
                  'crafting-with-fluid': Fluid_Assembly,
                  'chemistry': Fluid_Assembly,
                  'centrifuging': Assembly,
                  'oil-processing': Fluid_Assembly,
                  'drill': Drill}

    # list_function = {1: l_f(li), 2:l_f(li), 3:l_f(li)} # one item, at least 2 items, items with probability

    def __init__(self, time_in_seconds: float, output, inputs, name, category='crafting'):

        self.time = time_in_seconds
        self.output = output
        self.inputs = inputs
        self.category = category
        self.name = name


        #     try:
        #         p = o[2]
        #     except IndexError:
        #         p = 1
        #     try:
        #         item = Item.get_item_from_string(o[0])
        #     except KeyError:
        #         item = Item(o[0])
        #
        #     self.inputs[idx][1] = int(o[1])
        #
        # for idx, o in enumerate(output):
        #     try:
        #         p = o[2]
        #     except IndexError:
        #         p = 1
        for idx, i in enumerate(self.inputs):
            item = Item.get_item_from_string(i[0])
            self.inputs[idx][0] = item
            self.inputs[idx][1] = int(i[1])

        for idx, o in enumerate(self.output):
            item = Item.get_item_from_string(o[0])
            item.recipes.append(self)

            self.output[idx][1] = int(o[1])

        if self not in Recipe.recipes_list:
            Recipe.recipes_list.append(self)

    def __repr__(self):
        return f"{type(self).__name__}({self.time},{self.output},{self.inputs})"

    @property
    def output_quantity(self):
        # todo ensure this takes into account probability
        return self.output[0][1]

    # @property
    # def num_inputs(self):
    #     if not isinstance(self.inputs[0], tuple):
    #         return 1
    #     else:
    #         return len(self.inputs)
    #
    # @property
    # def num_outputs(self):
    #     if not isinstance(self.output[0], tuple):
    #         return 1
    #     else:
    #         return len(self.output)

    @staticmethod
    def get_tuple_from_list(li):
        items = []
        count = 0

        for idx, val in enumerate(li):
            # the order here is important
            if val == 'probability':
                items.pop()
                items.append([li[idx - 1], li[idx + 2], li[idx + 1]])
                count = 2
            elif count > 0:
                count -= 1
                continue
            elif val == 'item':
                items.append([li[idx + 1], li[idx + 2]])
                count = 2
            elif val == 'fluid':
                items.append([li[idx + 1], li[idx + 2]])
                count = 2
            # elif val == 'probability':
            #     items.push((li[idx - 1], li[idx + 2], li[idx + 1]))
            #     count = 2
            elif val == 'fluidbox_index':
                count = 1
                continue
            elif count == 0:
                try:
                    items.append([li[idx], li[idx+1]])
                    count += 1
                except IndexError as e:
                    print(e, li, idx)
                    break

        return items

    @staticmethod
    def get_recipe_from_string(s: str):
        item = Item.get_item_from_string(s)
        return item.recipes[0]


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

    def get_ratio(self, input_item):
        if len(self.inputs) == 1:
            if self.inputs[0][0].name == input_item:
                return int(self.inputs[0][1]) / self.output_quantity
        else:
            for item, quantity in self.inputs:
                if item.name == input_item:
                    return int(quantity) / self.output_quantity

    # def get_input_item(self):
    #     if len(self.inputs) == 1:
    #         yield self.inputs[0][0], self.inputs[0][1]
    #         return StopIteration
    #     else:
    #         for _input, quantity in self.inputs:
    #             yield _input, quantity
    #         return StopIteration


class Item(object):
    items_dict = {}
    is_raw = False
    is_fluid = False

    def __init__(self, name: str):
        self.name = name
        self.recipes = []
        if self.name not in Item.items_dict.keys():
            Item.items_dict[self.name] = self

        if issubclass(type(self), Liquid):
            self.is_fluid = True

    def __repr__(self):
        return f"{type(self).__name__}({self.name})"

    @property
    def has_multiple_recipes(self):
        return len(self.recipes) > 1

    @staticmethod
    def get_item_from_string(s: str):
        try:
            return Item.items_dict[s]
        except KeyError:
            item = Item(s)
            # item.recipes = [Recipe(1.0, [[item, 1]], [[item, 1]], item.name, 'drill')]
            # item.is_raw = True
            return item

    def get_recipe(self):
        try:
            return self.recipes[0]
        except IndexError:
            # base resource
            self.is_raw = True
            self.recipes.append(Recipe(1.0, [[self, 1]], [[self, 1]], self.name, 'drill'))
            return self.recipes[0]

    @staticmethod
    def create_raw_resources():
        for item in Item.items_dict.values():
            if len(item.recipes) == 0:
                item.is_raw = True
                # either need to get the recipes from file
                # or set a default one
                item.recipes = [[Recipe(1.0, [[item, 1]], [[item, 1]], item.name, 'drill')]]



# class Raw_Resource(Item):
#     """
#     Any item that doesn't have an assembler.
#     Examples would be copper/iron ore, oil, water etc.
#     """
#     is_raw = True
#
#     def __init__(self, name, machine_type_crafted_in=Drill, importance=False):
#         self.name = name
#         self.crafted_in = machine_type_crafted_in
#         self.importance = importance
#         self.recipes = []
#
#         if issubclass(type(self), Liquid):
#             self.is_fluid = True


class Fluid_Item(Item, Liquid):
    pass


# class Fluid_Raw_Resource(Raw_Resource, Liquid):
#     pass


class Fluid_Recipe(Recipe, Liquid):
    pass


class Multi_Craft(object):
    sub_total_dict = {}
    base_item_list = []
    recipe_list = []
    extra_recipe_list = []
    raw_resources = []
    multi_matrix = None

    @classmethod
    def add_to_class(cls, item, quantity):
        if item in cls.sub_total_dict:
            # print(f"dict - {item}: {cls.sub_total_dict[item]} + {quantity}")
            cls.sub_total_dict[item] = cls.sub_total_dict[item] + quantity

        else:
            # print(f"dict - {item}: {quantity}")
            cls.sub_total_dict[item] = quantity

        if item not in cls.base_item_list:
            # print(f"list - {item}")
            cls.base_item_list.append(item)

        for recipe in item.recipes:
            if recipe not in cls.recipe_list:
                # print(f"recipe - {recipe}")
                cls.recipe_list.append(recipe)
                for _item, quantity in recipe.inputs:
                    if _item not in cls.base_item_list:
                        cls.base_item_list.append(_item)

    @classmethod
    def build_matrix(cls):
        cls.multi_matrix = np.zeros((len(cls.base_item_list), len(cls.recipe_list)))
        cls.init_pop()
        cls.surplus_cols()
        cls.tax_row_and_col()
        cls.objective_function_row()
        cls.c_col()
        cls.output_col()

    @classmethod
    def init_pop(cls):
        """inital population of matrix"""
        for recipe in cls.recipe_list:
            cls.create_column_from_recipe(recipe, recipe.inputs, True)
            cls.create_column_from_recipe(recipe, recipe.output, False)

        for row_index in range(cls.multi_matrix.shape[0]-1):
            item = cls.base_item_list[row_index]
            if item.is_raw:
                cls.raw_resources.append(item)
                cls.extra_recipe_list.append(item)
                new_col = np.zeros((cls.multi_matrix.shape[0], 1))
                new_col[cls.base_item_list.index(item)] = 1
                cls.multi_matrix = np.hstack((cls.multi_matrix, new_col))

            for new_recipe in item.recipes:
                if new_recipe not in item.recipes:
                    # new_recipe = item.recipes[0]
                    new_matrix = np.zeros((cls.multi_matrix.shape[0], 1))
                    cls.multi_matrix = np.hstack((cls.multi_matrix, new_matrix))
                    cls.extra_recipe_list.append(new_recipe)
                    cls.create_column_from_recipe(new_recipe, new_recipe.output, False, 1)

    @classmethod
    def surplus_cols(cls):
        new_matrix = np.zeros((cls.multi_matrix.shape[0], len(cls.base_item_list)))
        for i in range(len(cls.base_item_list)):
            new_matrix[i, i] = 1
            cls.extra_recipe_list.append(f"s{i}")
        cls.multi_matrix = np.hstack((cls.multi_matrix, new_matrix))

    @classmethod
    def tax_row_and_col(cls):
        new_col = np.zeros((cls.multi_matrix.shape[0], 1))
        cls.multi_matrix = np.hstack((cls.multi_matrix, new_col))
        cls.extra_recipe_list.append("tax")
        new_row = np.zeros(cls.multi_matrix.shape[1])
        for i in range(len(cls.recipe_list)):
            new_row[i] = 1
        new_row[cls.extra_recipe_list.index("tax") + len(cls.recipe_list)] = 1
        cls.multi_matrix = np.vstack((cls.multi_matrix, new_row))

    @classmethod
    def objective_function_row(cls):
        abs_array = np.absolute(cls.multi_matrix[np.absolute(cls.multi_matrix) > 1])
        new_row = np.zeros(cls.multi_matrix.shape[1])
        for item in cls.raw_resources:
            offset = len(cls.recipe_list)
            if item.importance is True:
                new_row[offset + cls.raw_resources.index(item)] = -np.max(abs_array)
            else:
                new_row[offset + cls.raw_resources.index(item)] = -np.min(abs_array)
        new_row[cls.extra_recipe_list.index("tax") + len(cls.recipe_list)] = 1
        cls.multi_matrix = np.vstack((cls.multi_matrix, new_row))

    @classmethod
    def output_col(cls):
        new_col = np.zeros((cls.multi_matrix.shape[0], 1))
        for item, quantity in cls.sub_total_dict.items():
            new_col[cls.base_item_list.index(item)] = quantity
        cls.multi_matrix = np.hstack((cls.multi_matrix, new_col))
        cls.extra_recipe_list.append("output")

    @classmethod
    def c_col(cls):
        new_col = np.zeros((cls.multi_matrix.shape[0], 1))
        new_col[-1] = 1
        cls.multi_matrix = np.hstack((cls.multi_matrix, new_col))
        cls.extra_recipe_list.append("c")

    """negative for inputs, positive for outputs"""
    @classmethod
    def create_column_from_recipe(cls, recipe, in_out_list, negative=True, val=None):
        for item, quantity in in_out_list:
            if val is not None:
                quantity = val
            cls.multi_matrix[cls.base_item_list.index(item), cls.recipe_list.index(recipe)] = pow(-1, negative) * quantity

    @classmethod
    def simplex(cls):
        # todo divide pivot col values into the output col values - lowest = pivot row
        # todo make pivot value == 1 by multiplying the row by (1/value)
        # todo make other column values == 0 by taking away a multiple of the pivot row on each other row
        most_neg = np.int_(np.min(cls.multi_matrix[-1]))
        neg_col = list(cls.multi_matrix[-1]).index(most_neg)
        lowest_ratio = float('inf')
        for idx, row in enumerate(cls.multi_matrix):
            print(f"row {idx}: {row}")
            # lowest_ratio = min(lowest_ratio, )


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
    # Item.create_raw_resources()

# def read_or_write_data(should_init=False):
#     init_data()
#     if not should_init:
#         for fn in filenames:
#             pickle_read(fn)


def get_list_item_quantity(_list):
    for item, quantity in _list:
        yield Item.get_item_from_string(item), int(quantity)
    return StopIteration


def recipe_from_string(string):
        #https://regexr.com/5cj77
        #https://regexr.com/5cjci
        import re
        s = string.decode('ascii')
        time, output, inputs, name, category, next_item = 0.5, [], [], None, None, None
        pattern = re.compile(r'''((order){1}.*)|
                                    ((icon){1}.*)|
                                    ((enabled){1}.*)|
                                    ((allow_decomposition){1}.*)|
                                    ((requester_paste_multiplier){1}.*)|
                                    ((subgroup){1}.*)|
                                    ((crafting_machine_tint){1}.*)|
                                    ((primary){1}.*)|
                                    ((secondary){1}.*)|
                                    ((tertiary){1}.*)|
                                    ((quaternary){1}.*)|
                                    ((main_product){1}.*)''', re.VERBOSE)
        st = pattern.sub('', s)
        # print(st)
        pattern = re.compile(r'[A-Za-z0-9-_.]+')
        word_list = ['name', 'energy_required', 'result_count', 'ingredients',
                     'expensive', 'result', 'results', 'category']
        ingredients_list = ['name', 'type', 'amount']
        for word in pattern.finditer(st):
            # print(f'{word.group()}, {word.start()}')
            if next_item == 'expensive':
                # as far as ive seen, expensive is always the second listed recipe in the file
                break

            if next_item == 'category':
                category = str(word.group())

            if next_item == 'name':
                output.append(str(word.group()))
                next_item = None
                continue

            if next_item == 'results':
                if str(word.group()) in word_list:
                    if str(word.group()) in ingredients_list:
                        next_item = 'results'
                        continue
                    next_item = str(word.group())
                else:
                    if not str(word.group()) in ingredients_list:
                        output.append(str(word.group()))
                    continue

            if next_item == 'result_count':
                output.append(str(word.group()))
                next_item = None
                continue

            if next_item == 'energy_required':
                time = str(word.group())
                next_item = None
                continue

            if next_item == 'ingredients':
                if str(word.group()) in word_list:
                    if str(word.group()) in ingredients_list:
                        next_item = 'ingredients'
                        continue
                    next_item = str(word.group())
                else:
                    if not str(word.group()) in ingredients_list:
                        inputs.append(str(word.group()))
                    continue

            if str(word.group()) in word_list:
                next_item = str(word.group())
            else:
                next_item = None

        if category is None:
            # anything that can be crafted by hand can be crafted by machine
            category = 'crafting'


        # print(f'{output}, from {inputs}, in category:{category}, {time}s')
        name = output[0]
        if len(output) == 1:
            output.append('1')
        if len(output) == 2:
            output = Recipe.get_tuple_from_list(output)
        else:
            output = Recipe.get_tuple_from_list(output[1:])

        inputs = Recipe.get_tuple_from_list(inputs)
        Recipe(float(time), output, inputs, name, category)



def recipe_crawler(recipe: Recipe, total_dict=None, number_to_be_crafted=None, is_first_item=False):
    """
    dictionary is edited in place
    """
    if total_dict is None:
        total_dict = {}
    if number_to_be_crafted is None:
        number_to_be_crafted = recipe.output_quantity  # this breaks when there's more than 1 output

    if is_first_item:
        for item, quantity in recipe.output:
            add_to_dict(total_dict, item, number_to_be_crafted)
    for item, quantity in recipe.inputs:
        modified_quantity = number_to_be_crafted * recipe.get_ratio(item.name)
        if not item.is_raw:
            if item.has_multiple_recipes:  # handles oil production and anything that has multiple recipes
                Multi_Craft.add_to_class(item, modified_quantity)
            else:
                add_to_dict(total_dict, item, modified_quantity)
                recipe_crawler(Recipe.get_recipe(item), total_dict, modified_quantity)
        else:  # should handle raw resources like coal and ores
            if not is_first_item: # handles the case where the only item in the recipe chain is raw
                add_to_dict(total_dict, item, modified_quantity)
    return total_dict


init_data()

# read_or_write_data()
#
#
r = Recipe.get_recipe("production-science-pack")

t_d = recipe_crawler(r, None, 1000, True)
# recipe_crawler(n, t_d, 3.0)

# Multi_Craft.build_matrix()
# Multi_Craft.simplex()

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



