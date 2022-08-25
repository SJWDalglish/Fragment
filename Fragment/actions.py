import random
import abilities as ab


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


def attack(p: Player, o: Player, i: int, name: str, show=False):
    target = o.bots[i]
    if target.isBlank():
        target = o

    match name:
        case "Shunt":
            p.pp -= 1
            target.hp -= 1
            return 1

        case "Shock":
            p.pp -= 2
            target.hp -= 3
            return 1

        case "Energy Beam":
            p.pp -= 3
            target.hp -= 5
            return 1

        case "Giga Blast":
            p.pp -= 4
            target.hp -= 7
            return 1

        case "Double Jab":
            p.pp -= 1
            for j in range(2):
                target.hp -= cointoss()
            return 1

        case "Triple Tap":
            p.pp -= 2
            for j in range(3):
                target.hp -= 2 * cointoss()
            return 1

        case "Bullet Blitz":
            p.pp -= 3
            for j in range(5):
                target.hp -= 2 * cointoss()
            return 1

        case "Multi Missile":
            p.pp -= 4
            for j in range(5):
                target.hp -= 3 * cointoss()
            return 1

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
                ab.hp_ability(p,o,i,"Disruption")
                ab.pp_ability(o,i,"Sync")
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
            return 0

        case "Barrier":
            return 0

        case "Plan":
            return 0

    return 0
