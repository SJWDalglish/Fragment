import random
import abilities as ab
from card import Bot
from player import Player


class Action:
    def __init__(self, name: str, cost: int, desc: str, dmg: int):
        self.name = name
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


def cointoss():
    return random.choice([0, 1])


def rolld4():
    return random.randint(1,4)


def basic_attack(p: Player, o: Player, attacker, target, cost: int, dmg: int, name:str, show=False):
    p.pp -= cost

    dmg = max(0, dmg + attacker.atk_bonus - target.def_bonus)

    target.hp -= dmg

    for i in range(attacker.count("Scorch")):
        o.bots[rolld4()].hp -= 1

    if target.abilities.count("Whirlwind"):
        attacker.stunned = True

    if show:
        print(p.name, " did ", dmg, " damage to ", target.name, " using ", name)
    return 1


def roll_attack(p: Player, o: Player, attacker, target, cost: int, coins: int, coin_dmg: int, name: str, show=False):
    p.pp -= cost

    dmg = 0
    for i in range(coins):
        dmg += coin_dmg * cointoss()
    dmg = max(0, dmg + attacker.atk_bonus - target.def_bonus)

    target.hp -= dmg

    for i in range(attacker.count("Scorch")):
        o.bots[rolld4()].hp -= 1

    if target.abilities.count("Whirlwind"):
        attacker.stunned = True

    if show:
        print(p.name, " did ", dmg, " damage to ", target.name, " using ", name)
    return 1


def attack(p: Player, o: Player, i: int, name: str, show=False):
    attacker = p.bots[i]
    target = o.bots[i]
    if target.isBlank():
        target = o

    match name:
        case "Shunt":
            return basic_attack(p, o, attacker, target, 1, 1, "Shunt", show)

        case "Shock":
            return basic_attack(p, o, attacker, target, 2, 3, "Shock", show)

        case "Energy Beam":
            return basic_attack(p, o, attacker, target, 3, 5, "Energy Beam", show)

        case "Giga Blast":
            return basic_attack(p, o, attacker, target, 4, 7, "Giga Blast", show)

        case "Double Jab":
            return roll_attack(p, o, attacker, target, 1, 2, 1, "Double Jab", show)

        case "Triple Tap":
            return roll_attack(p, o, attacker, target, 2, 3, 2, "Triple Tap", show)

        case "Bullet Blitz":
            return roll_attack(p, o, attacker, target, 3, 5, 2, "Bullet Blitz", show)

        case "Multi Missile":
            return roll_attack(p, o, attacker, target, 4, 5, 3, "Multi Missile", show)

        case "Cure Wounds":
            p.pp -= 1
            p.bots[rolld4()].hp += 2
            return 1

        case "Incentivize":
            p.pp -= 1
            n = rolld4()
            for j in range(n):
                card = p.deck.pop()
                p.hand.append(card)
                ab.hp_ability(p, o, i, "Disruption")
                ab.pp_ability(o, i, "Sync")
            return 1

        case "Fireball":
            p.pp -= 1
            o.bots[rolld4()].hp -= 2
            return 1

        case "Twister":
            p.pp -= 1
            j = rolld4()
            tmp_bot = o.bots[i]
            o.bots[i] = o.bots[j]
            o.bots[j] = tmp_bot
            return 1

        case "Deplete":
            p.pp -= 1
            n = rolld4()
            p.bots[i].atk_bonus += n
            return 1

        case "Barrier":
            p.pp -= 1
            n = rolld4()
            p.bots[n].def_bonus = 1000
            return 1

        case "Plan":
            return 0

    return 0
