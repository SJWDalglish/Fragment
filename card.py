types = ["Acquire", "Augment", "Consume", "Convert", "Cultivate", "Preserve"]
resource_types = ["Biomass", "Power Cell", "Fossil Fuel", "Radioactive Material", "Weather Event"]


class Card(object):
    def __init__(self, name: str, resource: str, cost: int, hp: int, ability1: str, ability2="None"):
        self.name = name
        self.resource = resource
        self.cost = cost
        self.hp = hp
        self.ability1 = ability1
        self.ability2 = ability2

    def display(self):
        print("\n------\nGenerator: " + self.name)
        print("Resource: " + self.resource)
        print("Cost: " + str(self.cost))
        print("HP: " + str(self.hp))
        print("Ability 1: " + self.ability1)
        print("Ability 2: " + self.ability2)
        print("------")

    def listify(self):
        return [self.name, type(self).__name__, str(self.cost) + "PP", str(self.hp) + "HP", self.ability1,
                self.ability2]  # Removed self.ability


class Generator(Card):
    def __init__(self, name: str, resource: str, cost: int, hp: int, ability: str):
        super().__init__(name, resource, cost, hp, ability)


class Frame(Card):
    def __init__(self, name: str, resource: str, cost: int, hp: int, ability1: str, ability2: str):
        super().__init__(name, resource, cost, hp, ability1, ability2)


class Part(Card):
    def __init__(self, name: str, cost: int, hp: int, ability: str):
        type = "None"
        super().__init__(name, type, cost, hp, ability)


class Bot:
    def __init__(self, frame: Frame, position=None):
        self.name = frame.name
        self.type = None
        self.current_hp = frame.hp
        self.max_hp = frame.hp
        self.abilities = [frame.ability1, frame.ability2]
        self.components = [frame]
        self.position = position
        self.resources = []
        self.resource = "None"

    def power(self, gen: Generator):
        self.resource = gen.resource
        self.abilities.append(gen.ability1)
        self.components.insert(0, gen)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        self.resources = ['Power Cell']
        if self.type == 'Augment':
            self.resources.append('Radioactive Material')
        elif self.type == 'Consume':
            self.resources.append('Fossil Fuel')
        elif self.type == "Convert":
            self.resources.append('Weather Event')
        elif self.type == "Cultivate":
            self.resources.append('Biomass')

    def display_name(self):
        print(self.name)

    def display(self):
        print("\n------\nBot: " + self.name)
        print("HP: " + str(self.current_hp) + "/" + str(self.max_hp))
        print("Effects:")
        for i in range(len(self.abilities)):
            print("   [" + str(i) + "] " + self.abilities[i])
        print("------")

    def display_abilities(self):
        for i in range(len(self.abilities)):
            print("Ability " + str(i + 1) + ": " + self.abilities[i])

    def dmg(self, dmg: int):
        self.current_hp -= dmg

    def gen(self, pow: int):
        self.pp += pow

    def upgrade(self, part: Part):
        num_components = len(self.components)
        self.components.insert(num_components - 1, part)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        self.max_hp += part.hp
        self.current_hp += part.hp
        self.abilities.append(part.ability1)

    def stringify(self):
        return self.name + "\nHP: " + str(self.current_hp) + "/" + str(self.max_hp)

    def isblank(self):
        if self.name == 'BlankBot':
            return True
        return False
