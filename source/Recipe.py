from source.Item import Item
from source.Machine import *
from source.Multi_Craft import *

class Recipe(object):
    recipes_list = []


    def __init__(self, time_in_seconds: float, output, inputs, name, category='crafting'):

        self.time = time_in_seconds
        self.output = output
        self.inputs = inputs
        self.category = category
        self.name = name

        for idx, o in enumerate(output):
            #this wont work for both probability and fluid items
            try:
                p = o[2]
            except IndexError:
                p = 1

            item = Item.get_item_from_string(o[0])
            if not self.is_raw:
                item.append_recipe(self)

            self.output[idx][0] = item
            self.output[idx][1] = int(o[1])

        for idx, i in enumerate(self.inputs):
            item = Item.get_item_from_string(i[0])
            self.inputs[idx][0] = item
            self.inputs[idx][1] = int(i[1])

        if self not in Recipe.recipes_list:
            Recipe.recipes_list.append(self)



    def __repr__(self):
        return f"{type(self).__name__}({self.time},{self.output},{self.inputs})"

    @property
    def output_quantity(self):
        # todo ensure this takes into account probability
        # try:
        #     prob = self.output[0][2]
        #     return self.output[0][1] * prob
        return self.output[0][1]

    @property
    def is_raw(self):
        return self.inputs == self.output

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
                items.append([Item(li[idx + 1]), li[idx + 2]])
                count = 2
            elif val == 'fluid':
                items.append([Liquid(li[idx + 1]), li[idx + 2]])
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


def add_to_dict(dict_to_add_to, item, quantity):
    if item not in dict_to_add_to.keys():
        dict_to_add_to[item] = quantity
    else:
        cur_quantity = dict_to_add_to[item]
        dict_to_add_to[item] = cur_quantity + quantity


def recipe_from_string(string):
    # https://regexr.com/5cj77
    # https://regexr.com/5cjci
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
                r = Recipe.get_recipe(item)
                if not r.is_raw:
                    recipe_crawler(r, total_dict, modified_quantity)
        else:  # should handle raw resources like coal and ores
            if not is_first_item:  # handles the case where the only item in the recipe chain is raw
                # disabled because it doubles the output of raw resources
                add_to_dict(total_dict, item, modified_quantity)
                pass
    return total_dict
