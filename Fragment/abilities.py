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
    health_gained = 2 * player.bots[i].abilities.count("Disruption")
    player.bots[i].current_hp += health_gained
    player.bots[i].max_hp += 2 * health_gained
    if show:
        print(player.name, "'s bot ", player.bots[i].name, " syphoned ", health_gained, " health from the scrapheap.")


def refraction(player: Player, i: int, show=False):
    health_gained = 2 * player.bots[i].abilities.count("Refraction")
    player.bots[i].current_hp += health_gained
    player.bots[i].max_hp += health_gained
    if show:
        print(player.name, "'s bot ", player.bots[i].name, " generated ", health_gained, " health from the wind as they moved.")



def burn(player: Player, i: int, show=False):
    health_gained = 2 * player.bots[i].abilities.count("Burn")
    player.bots[i].current_hp += health_gained
    player.bots[i].max_hp += health_gained
    if show:
        print(player.name, "'s bot ", player.bots[i].name, " smelted ", health_gained, " health from mined resources.")


def rain_recollection(player: Player, i: int, show=False):
    health_gained = 2 * player.bots[i].abilities.count("Rain Recollection")
    player.bots[i].current_hp += health_gained
    player.bots[i].max_hp += health_gained
    if show:
        print(player.name, "'s bot ", player.bots[i].name, " collected ", health_gained, " health from moving showers.")


def leech(player: Player, i: int, show=False):
    health_gained = 2 * player.bots[i].abilities.count("Leech")
    player.bots[i].current_hp += health_gained
    player.bots[i].max_hp += health_gained
    if show:
        print(player.name, "'s bot ", player.bots[i].name, " leeched ", health_gained, " health from the new bot.")



def reallocate(opponent: Player, i: int, show=False):
    if opponent.bots[i].abilities.count("Reallocate") > 0:
        opponent.pp += special_pp_gained
        if show:
            print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                special_pp_gained) + 'pp from opposing bot.')

