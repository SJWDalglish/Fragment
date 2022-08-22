from player import Player

# Ability values
pp_gained = 2
special_pp_gained = 1


class Ability:
    def __init__(self, name: str, ability_type: str, cost: int, desc: str, dmg: int):
        self.name = name
        self.ability_type = ability_type
        self.cost = cost
        self.desc = desc
        self.dmg = dmg

    def display(self):
        print("\n------\nAbility: ", self.name)
        print("Type: ", self.ability_type)
        if self.ability_type == "Active":
            print("Cost: ", self.cost)
            print("Damage: ", self.dmg)
        print("Effect: " + self.desc)
        print("------")


def disruption(player: Player, i: int, show=False):
    player.pp += special_pp_gained * player.bots[i].abilities.count("Disruption")
    if show:
        print(player.name, "'s bot ", player.bots[i].name, " syphoned ", special_pp_gained, " from the scrapheap.")


def reallocate(opponent: Player, i: int, show=False):
    if opponent.bots[i].abilities.count("Reallocate") > 0:
        opponent.pp += special_pp_gained
        if show:
            print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                special_pp_gained) + 'pp from opposing bot.')

