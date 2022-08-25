from player import Player


class Ability:
    def __init__(self, name: str, ability_type: str, cost: int, desc: str, dmg: int):
        self.name = name
        self.ability_type = ability_type
        self.cost = cost
        self.desc = desc

    def display(self):
        print("\n------\nAbility: ", self.name)
        print("Type: ", self.ability_type)
        if self.ability_type == "Active":
            print("Cost: ", self.cost)
            print("Damage: ", self.dmg)
        print("Effect: " + self.desc)
        print("------")


def hp_ability(p: Player, o: Player, bot_num: int, name: str, show=False):
    if p.bots[bot_num].stunned:
        return 0
    hp_gained = p.default_hp_gained * p.bots[bot_num].abilities.count(name)
    p.bots[bot_num].current_hp += hp_gained
    reallocate(o, bot_num, show)
    if show:
        print(p.name, "'s bot ", p.bots[bot_num].name, " regained ", hp_gained, " HP using ", name)


def pp_ability(p: Player, bot_num: int, name: str, show=False):
    if p.bots[bot_num].stunned:
        return 0
    pp_gained = p.default_pp_gained * p.bots[bot_num].abilities.count(name)
    p.pp += pp_gained
    if show:
        print(p.name, "'s bot ", p.bots[bot_num].name, " generate ", pp_gained, " PP using ", name)


def reallocate(o: Player, i: int, show=False):
    if o.bots[i].stunned:
        return 0
    pp_gained = o.special_pp_gained * o.bots[i].abilities.count("Reallocate")
    o.pp += pp_gained
    if show:
        print(o.name + "'s bot " + o.bots[i].name + ' syphoned ' + str(pp_gained) + 'PP from opposing bot.')

