import numpy as np

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
        if cls.sub_total_dict == {}:
            return None
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
            # if item.importance is True:
            #     new_row[offset + cls.raw_resources.index(item)] = -np.max(abs_array)
            # else:
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
