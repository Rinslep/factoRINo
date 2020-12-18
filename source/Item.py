class Item(object):
    items_dict = {}
    is_fluid = False

    def __init__(self, name: str):
        self.name = name
        self.recipes = []
        self.is_raw = False
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
        if type(s) is Item:
            return s
        try:
            return Item.items_dict[s]
        except KeyError:
            item = Item(s)
            return item

    def get_recipe(self):
        try:
            return self.recipes[0]
        except IndexError:
            # base resource
            self.raw(True)
            from source.Recipe import Recipe
            if self.is_fluid:
                machine = 'pump'
            else:
                machine = 'drill'
            self.append_recipe(Recipe(1.0, [[self, 1]], [[self, 1]], self.name, machine))
            return self.recipes[0]

    def raw(self, bool):
        self.is_raw = bool

    def append_recipe(self, recipe):
        if recipe in self.recipes:
            pass
        else:
            if self.is_raw:
                self.recipes = [recipe]
            else:
                self.recipes.append(recipe)

    @property
    def connected_items(self):
        l = []
        r = self.get_recipe()
        for item, q in r.inputs:
            if item not in l:
                l.append(item)
        for item, q in r.output:
            if item not in l:
                l.append(item)

        return l

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


class Liquid(Item):
    def __init__(self, name):
        self.is_liquid = True
        super(Liquid, self).__init__(name)
