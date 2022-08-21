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
