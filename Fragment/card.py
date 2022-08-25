# Card types
types = ["Acquire", "Augment", "Consume", "Convert", "Cultivate", "Preserve"]
resource_types = ["Biomass", "Power Cell", "Fossil Fuel", "Radioactive Material", "Weather Event"]


class Card(object):
    def __init__(self, name: str, deck: str, cost: int, hp: int, desc: str, ability1="None", ability2="None", action1="None", action2="None"):
        self.name = name
        self.cost = cost
        self.deck = deck
        self.hp = hp
        self.desc = desc
        self.ability1 = ability1
        self.ability2 = ability2
        self.action1 = action1
        self.action2 = action2

    def display(self):
        print("\n------\nGenerator: " + self.name)
        print("Resource: " + self.resource)
        print("Cost: " + str(self.cost))
        print("HP: " + str(self.hp))
        print("Ability 1: " + self.ability1)
        print("Ability 2: " + self.ability2)
        print("------")

    def listify(self, discount=0):
        return [self.name, type(self).__name__, str(min(0, self.cost - discount)) + "PP", str(self.hp) + "HP", self.ability1,
                self.ability2]


class Generator(Card):
    def __init__(self, name: str, deck: str, cost: int, hp: int, desc: str, ability1: str):
        super().__init__(name, deck, cost, hp, desc, ability1)


class Frame(Card):
    def __init__(self, name: str, deck: str, cost: int, hp: int, desc: str, action1: str, action2: str):
        super().__init__(name, deck, cost, hp, desc, action1=action1, action2=action2)


class Part(Card):
    def __init__(self, name: str, cost: int, hp: int, desc: str, action: str):
        super().__init__(name, "All", cost, hp, action1=action)


class Mechanic(Card):
    def __init__(self, name: str, cost: int, desc: str):
        super().__init__(name, "All", cost, 0, desc)


class Bot:
    def __init__(self, frame: Frame, position=None):
        self.name = frame.name
        self.type = None
        self.current_hp = frame.hp
        self.max_hp = frame.hp
        self.abilities = []
        self.actions = [frame.action1, frame.action2]
        self.components = [frame]
        self.position = position
        self.stunned = False
        self.atk_bonus = 0
        self.def_bonus = 0

    def power(self, gen: Generator):
        self.abilities.append(gen.ability1)
        if ability2 != "None":
            self.abilities.append(gen.ability2)
        self.components.insert(0, gen)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        # self.resources = ['Power Cell']
        # if self.type == 'Augment':
        #     self.resources.append('Radioactive Material')
        # elif self.type == 'Consume':
        #     self.resources.append('Fossil Fuel')
        # elif self.type == "Convert":
        #     self.resources.append('Weather Event')
        # elif self.type == "Cultivate":
        #     self.resources.append('Biomass')

    def display_name(self):
        print(self.name)

    def display(self):
        print("\n------\nBot: " + self.name)
        print("HP: " + str(self.current_hp) + "/" + str(self.max_hp))
        print("Effects:")
        for i in range(len(self.abilities)):
            print("   [" + str(i) + "] " + self.abilities[i])
        print("------")

    def display_actions(self):
        for i in range(len(self.actions)):
            print("Action " + str(i + 1) + ": " + self.actions[i])

    def display_abilities(self):
        for i in range(len(self.abilities)):
            print("Ability " + str(i + 1) + ": " + self.abilities[i])

    def dmg(self, dmg: int):
        self.current_hp -= dmg

    def upgrade(self, part: Part):
        num_components = len(self.components)
        self.components.insert(num_components - 1, part)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        self.max_hp += part.hp
        self.current_hp += part.hp
        self.actions.append(part.action1)

    def stringify(self):
        return self.name + "\nHP: " + str(self.current_hp) + "/" + str(self.max_hp)

    def isblank(self):
        if self.name == 'BlankBot':
            return True
        return False

    def stun(self):
        self.stunned = True

    def awaken(self):
        self.stunned = False
