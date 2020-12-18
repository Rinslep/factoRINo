from source.Item import Liquid


class Machine(object):
    machines_dict = {}

    def __init__(self, name: str, crafting_speed: float, module_slots: int, size=3, recipe=None):
        self.name = name
        self.crafting_speed = crafting_speed
        self.module_slots = module_slots
        self.size = size
        self.recipe = recipe
        self.beacons = {}


        if self.name not in Machine.machines_dict.keys():
            Machine.machines_dict[self.name] = self

    def __repr__(self):
        return "{}('{}',{},{})".format(type(self).__name__, self.name, self.crafting_speed, self.module_slots)

    def add_beacon(self, beacon):
        if beacon.id not in self.beacons.keys():
            self.beacons[beacon.id] = beacon.value

    @property
    def machine_multiplier(self):
        prod_multi = 1.0
        return self.crafting_speed * prod_multi

    @classmethod
    def pos_machines(cls, recipe):
        return [machine for machine in machine_categories[recipe.category].machines]

    @classmethod
    def machines_needed(cls, r, q, timeframe):
        # returns in machines per seconds
        pos_machine = {}
        # get all applicable machines for that recipe
        for machine in machine_categories[r.category].machines:
            # pos_machine.append(machine)
            pos_machine[machine.name] = ((q * r.time) / (r.output[0][1] * machine.machine_multiplier)) / timeframe

        # mn = icr * time * (1/items) * (1/speed) * (1/prod)
        # print(r.name, q, pos_machine)
        for m, v in pos_machine.items():
            print(r.name, round(q, 3), m, round(v, 3))



class Drill(Machine):
    # all but uranium
    machines = []

    def __init__(self, *args):
        super(Drill, self).__init__(*args)
        if self not in Drill.machines:
            Drill.machines.append(self)


class Drill_Using_Fluid(Machine):
    # used only for uranium mining
    pass


class Pump(Machine):
    # oil and water
    machines = []

    def __init__(self, *args):
        super(Pump, self).__init__(*args)
        if self not in Pump.machines:
            Pump.machines.append(self)


class Assembly(Machine):
    machines = []

    def __init__(self, *args):
        super(Assembly, self).__init__(*args)
        if self not in Assembly.machines:
            Assembly.machines.append(self)


class Centrifuge(Assembly):
    machines = []

    def __init__(self, *args):
        super(Assembly, self).__init__(*args)
        if self not in Centrifuge.machines:
            Centrifuge.machines.append(self)


class Fluid_Assembly(Assembly):
    machines = []

    def __init__(self, *args):
        super(Assembly, self).__init__(*args)
        if self not in Fluid_Assembly.machines:
            Fluid_Assembly.machines.append(self)


class Rocket_Assembly(Assembly):
    machines = []
    def __init__(self, *args):
        super(Assembly, self).__init__(*args)
        if self not in Rocket_Assembly.machines:
            Rocket_Assembly.machines.append(self)


class Furnace(Assembly):
    machines = []

    def __init__(self, *args):
        super(Assembly, self).__init__(*args)
        if self not in Furnace.machines:
            Furnace.machines.append(self)


machine_categories = {'rocket-building': Rocket_Assembly,
                      'crafting': Assembly,
                      'crafting-with-fluid': Fluid_Assembly,
                      'chemistry': Fluid_Assembly,
                      'centrifuging': Centrifuge,
                      'oil-processing': Fluid_Assembly,
                      'smelting': Furnace,
                      'drill': Drill,
                      'pump': Pump}

silo = Rocket_Assembly('rocket-silo', 1.0, 4, 7)
a1 = Assembly('assembly-machine-1', 0.5, 0)
a2 = Assembly('assembly-machine-2', 0.75, 2)
a3 = Assembly('assembly-machine-3', 1.25, 4)
bf = Furnace('stone-furnace', 1.0, 0, 2)
sf = Furnace('steel-furnace', 2.0, 0)
ef = Furnace('electric-furnace', 2.0, 2)
cp = Fluid_Assembly('chemical-plant', 1.0, 3)
ed = Drill('electric-mining-drill', 0.5, 3)
pj = Pump('pumpjack', 0.5, 2)



