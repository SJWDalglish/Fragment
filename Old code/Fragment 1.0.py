import pandas as pd
from tabulate import tabulate
import numpy as np


actions = pd.read_csv('Fragment 1.0 CSV Files/Abilities.csv')
effects = pd.read_csv('Fragment 1.0 CSV Files/Frames.csv')
gens = pd.read_csv('Fragment 1.0 CSV Files/Genserators.csv')
cells = pd.read_csv('Fragment 1.0 CSV Files/Parts.csv')




class Action:
    def __init__(self, name: str, cost: int, dmg: int, targets: int):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.targets = targets

    def display(self):
        print("\n------\nAction: " + self.name)
        print("Cost: " + str(self.cost))
        print("Damage: " + str(self.dmg))
        print("Targets: " + str(self.targets))
        print("------")


class Generator:
    def __init__(self, name:  str, type: str, resource: str, cost: int, hp: int, actions: []):
        self.name = name
        self.type = type
        self.cost = cost
        self.hp = hp
        self.actions = actions
        self.resource = resource

    def display(self):
        print("\n------\nGenerator: " + self.name)
        # print("Type: " + self.type)
        print("Cost: " + str(self.cost))
        print("HP: " + str(self.hp))
        print("Resource: " + self.resource)
        print("Actions: ")
        for i in range(len(self.actions)):
            print("   [" + str(i) + "] " + self.actions[i].name)
        print("------")


class SoulCell:
    def __init__(self, name, type, cost, hp, effects):
        self.name = name
        self.type = type
        self.cost = cost
        self.hp = hp
        self.effects = effects

    def display(self):
        print("\n------\nCell: " + self.name)
        # print("Type: " + self.type)
        print("Cost: " + str(self.cost))
        print("HP: " + str(self.hp))
        print("Effects:")
        for i in range(len(self.effects)):
            print("   [" + str(i) + "] " + self.effects[i].name)
        print("------")


class Part:
    def __init__(self, name, cost, hp, effects, actions):
        self.name = name
        self.cost = cost
        self.hp = hp
        self.effects = effects
        self.actions = actions

    def display(self):
        print("\n------\nPart: " + self.name)
        print("Cost: " + str(self.cost))
        print("HP: " + str(self.hp))
        print("Effects:")
        for i in range(len(self.effects)):
            print("   [" + str(i) + "] " + self.effects[i].name)
        print("Actions: ")
        for i in range(len(self.actions)):
            print("   [" + str(i) + "] " + self.actions[i].name)
        print("------")


class Bot:
    def __init__(self, gen: Generator, cel: SoulCell, res, pp=0):
        if gen.type != cel.type:
            print("Mismatched types. Bot not Built.")
        self.name = gen.name + cel.name
        self.type = gen.type
        self.current_hp = gen.hp + cel.hp
        self.max_hp = gen.hp + cel.hp
        self.actions = gen.actions
        self.effects = cel.effects
        self.pp = pp
        self.resource = gen.resource
        self.components = [gen, cel]
        self.resources = res

    def displayName(self):
        print(self.name)

    def display(self):
        print("\n------\nBot: " + self.name)
        # print("Type: " + self.type)
        print("HP: " + str(self.current_hp) + "/" + str(self.max_hp))
        print("PP: " + str(self.pp))
        print("Effects:")
        for i in range(len(self.effects)):
            print("   [" + str(i) + "] " + self.effects[i].name)
        print("Actions: ")
        for i in range(len(self.actions)):
            print("   [" + str(i) + "] " + self.actions[i].name)
        print("------")

    def displayActions(self):
        for i in range(len(self.actions)):
            print("Action " + str(i+1) + ": ")
            self.actions[i].display()

    def dmg(self, dmg: int):
        self.hp -= dmg

    def gen(self, pow: int):
        self.pp += pow

    def upgrade(self, part):
        numComponents = len(self.components)
        self.components.insert(numComponents - 1, part)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        self.hp += part.hp
        self.actions += part.actions
        self.effects += part.effects


def prepCards():
    raw_actions = pd.read_csv('CSV/Actions.csv')
    raw_effects = pd.read_csv('CSV/Effects.csv')
    raw_gens = pd.read_csv('CSV/Gens.csv')
    raw_cells = pd.read_csv('CSV/Cells.csv')

    actions = []
    for index, rows in raw_actions.iterrows():
        actions.append(Action(rows['Action Name'], rows['Action Cost'], rows['Action Effect'], rows['Targets']))


def displayHand(hand: []):
    for card in hand:
        card.display()




if __name__ == '__main__':
    a1 = Action(name="Dash Kick", cost=1, dmg=3, targets=1)
    a1.display()
    g1 = Generator(name="Herba", type="Cultivate", cost=1, hp=4, actions=[a1], resource="Plantlife")
    g1.display()
    c1 = SoulCell(name="ling", type="Cultivate", cost=1, hp=4, effects=[])
    c1.display()
    p1 = Part(name="cyclo", cost=1, hp=1, effects=[], actions=[a1])
    p1.display()
    b1 = Bot(g1, c1, [], 0)
    b1.display()
    b1.upgrade(p1)
    b1.display()



