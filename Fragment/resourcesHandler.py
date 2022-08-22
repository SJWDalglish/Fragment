from random import randint, shuffle
resource_types = ["Biomass", "Power Cell", "Fossil Fuel", "Radioactive Material", "Weather Event"]
num_resources = 6


class ResourceHandler:
    def __init__(self):
        self.deck = []
        for resource in resource_types:
            for i in range(num_resources):
                self.deck.append(resource)
        shuffle(self.deck)
        self.pile = self.deck[:4]
        del self.deck[:4]

    def show_pile(self):
        print('\n' + " | ".join(self.pile) + '\n')

    def list_pile(self):
        resource_pile = ""
        for i in range(4):
            resource_pile += "\n[" + str(i) + "]" + self.pile[i]
        print(resource_pile)

    def swap_resource(self, i: int):
        old_resource = self.pile[i]
        new_resource = self.deck.pop()
        self.pile[i] = new_resource
        self.deck.insert(0, old_resource)
        return old_resource, new_resource

    def swap_resources(self):
        output = []
        for i in range(4):
            o, n = self.swap_resource(i)
            output.append([o, n])
        return output
