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