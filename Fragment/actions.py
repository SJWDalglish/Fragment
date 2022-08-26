import random
import abilities as ab
from player import Player, blank_bot


def cointoss():
    return random.choice([0, 1])


def rolld4():
    return random.randint(1, 4)


def basic_attack(p: Player, o: Player, i: int, cost: int, dmg: int, name: str, show=False):
    if p.pp < cost:
        if show:
            print("Not enough PP!")
        return 0
    p.pp -= cost

    dmg = max(0, dmg + p.bots[i].atk_bonus - o.bots[i].def_bonus)

    if o.bots[i].isblank():
        o.hp -= dmg
        if show:
            print(p.name, " did ", dmg, " damage to ", o.name, " using ", name)
    else:
        o.bots[i].current_hp -= dmg
        if show:
            print(p.name, " did ", dmg, " damage to ", o.bots[i].name, " using ", name)
        if o.bots[i].current_hp <= 0:
            destroy_bot(o, p, i, show)

    for j in range(p.bots[i].abilities.count("Scorch")):
        t2 = rolld4()
        o.bots[t2].current_hp -= 1
        if show:
            print(p.name, " did ", 1, " damage to ", o.bots[t2].name, " using Scorch")
        if o.bots[i].current_hp <= 0:
            destroy_bot(o, p, i, show)

    if o.bots[i].abilities.count("Whirlwind") > 1:
        p.bots[i].stunned = True
        if show:
            print(o.bots[i].name, " stunned ", p.bots[i].name, " using Whirlwind")

    return 1


def destroy_bot(p: Player, o: Player, dead_bot_num: int, show=False):
    db = p.bots[dead_bot_num]

    if db.current_hp > 0:
        print("Error: Tried destroying a bot with health remaining.")
        return 0

    p.discard.extend(db.components)
    p.bots[dead_bot_num] = blank_bot

    for i in range(4):
        p.pp += p.bots[i].count("Recycle") * p.default_pp_gained
        o.pp += o.bots[i].count("Spare Parts") * o.default_pp_gained
        o.bots[i].atk_bonus += p.bots[i].count("Harvest")

    return 1


def roll_dmg(coins: int, coin_dmg: int):
    dmg = 0
    for i in range(coins):
        dmg += coin_dmg * cointoss()
    return dmg


def attack(p: Player, o: Player, i: int, name: str, show=False):
    attacker = p.bots[i]
    target = o.bots[i]
    if target.isblank():
        target = o

    match name:
        case "Shunt":
            return basic_attack(p, o, i, 1, 1, "Shunt", show)

        case "Shock":
            return basic_attack(p, o, i, 2, 3, "Shock", show)

        case "Energy Beam":
            return basic_attack(p, o, i, 3, 5, "Energy Beam", show)

        case "Giga Blast":
            return basic_attack(p, o, i, 4, 7, "Giga Blast", show)

        case "Double Jab":
            return basic_attack(p, o, i, 1, roll_dmg(2, 1), "Double Jab", show)

        case "Triple Tap":
            return basic_attack(p, o, i, 2, roll_dmg(3, 1), "Triple Tap", show)

        case "Bullet Blitz":
            return basic_attack(p, o, i, 3, roll_dmg(5, 2), "Bullet Blitz", show)

        case "Multi Missile":
            return basic_attack(p, o, i, 4, roll_dmg(5, 3), "Multi Missile", show)

        case "Cure Wounds":
            p.pp -= 1
            j = rolld4() - 1
            p.bots[j].current_hp += 2
            if show:
                print(p.bots[i].name, "healed", p.bots[j].name, "for 2HP using Cure Wounds")
            return 1

        case "Incentivize":
            p.pp -= 1
            n = rolld4()
            for j in range(n):
                card = p.deck.pop()
                p.hand.append(card)
                ab.hp_ability(p, o, i, "Disruption")
                ab.pp_ability(o, i, "Sync")
            if show:
                print(p.bots[i].name, "healed", p.bots[j].name, "for 2HP using Cure Wounds")
            return 1

        case "Fireball":
            p.pp -= 1
            j = rolld4()-1
            o.bots[j].current_hp -= 2
            if show:
                print(p.bots[i].name, "scorched", o.bots[j].name, "for 2 DMG using Fireball")
            return 1

        case "Twister":
            p.pp -= 1
            j = rolld4() - 1
            tmp_bot = o.bots[i]
            o.bots[i] = o.bots[j]
            o.bots[j] = tmp_bot
            if show:
                print(p.bots[i].name, "moved", o.bots[j].name, "for using Twister")
            return 1

        case "Deplete":
            p.pp -= 1
            n = rolld4()
            p.bots[i].atk_bonus += n
            if show:
                print(p.bots[i].name, "gained", n, "attack bonus using Deplete")
            return 1

        case "Barrier":
            p.pp -= 1
            j = rolld4() - 1
            p.bots[j].def_bonus = 1000
            if show:
                print(p.bots[i].name, "protected", p.bots[j].name, "for 2HP using Barrier")
            return 1

        case "Plan":
            return 0

    return 0
