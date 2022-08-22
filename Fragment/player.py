from tabulate import tabulate
from random import randint, shuffle
from card import *
from resourcesHandler import *
import abilities as ab

blank_bot = Bot(Frame("Bot", "None", 0, 0, "None", "None"))


class Player:
    # Action costs
    _start_pp = 0
    _start_hp = 20
    _draw_cost = 1
    _resource_swap_cost = 1
    _refresh_cost = 2
    _move_cost = 1

    def __init__(self, name: str, resource: str, deck, ai=False, strategy=[1, 1, 1, 1, 1, 1]):
        self.name = name
        self.resource = resource
        self.hp = _start_hp
        self.deck = deck
        self.bots = [blank_bot, blank_bot, blank_bot, blank_bot]
        self.hand = []
        self.discard = []
        self.pp = _start_pp
        self.ai = ai
        self.strategy = strategy
        self.draw_cost = _draw_cost
        self.resource_swap_cost = _resource_swap_cost
        self.refresh_cost = _refresh_cost
        self.move_cost = _move_cost
        self.actions = []

    def get_resource_types(self):
        output = ['Power Cell']
        if self.resource == 'Augment':
            output.append('Radioactive Material')
        elif self.resource == 'Consume':
            output.append('Fossil Fuel')
        elif self.resource == "Convert":
            output.append('Weather Event')
        elif self.resource == "Cultivate":
            output.append('Biomass')
        return output

    def count_cards(self):
        card_count = [0, 0, 0, 0]
        for card in self.hand:
            if isinstance(card, Generator):
                card_count[0] += 1
            if isinstance(card, Frame):
                card_count[1] += 1
            if isinstance(card, Part):
                card_count[2] += 1
        for bot in self.bots:
            if not bot.isblank():
                card_count[3] += 1
        return card_count

    def get_hand(self, class_name=Card):
        cards = []
        for card in self.hand:
            if isinstance(card, class_name):
                cards.append(card)
        return cards

    def show_hand(self, class_name=Card, discount=0):
        cards = []
        card_list = []
        for card in self.hand:
            if isinstance(card, class_name):
                card_formatted = card.listify(discount)
                card_formatted.insert(0, str(len(card_list) + 1))
                card_list.append(card_formatted)
                cards.append(card)
        print(tabulate(card_list))
        return cards

    def show_bots(self):
        cards = []
        bot_list = []
        for bot in self.bots:
            if bot.name == "BlankBot":
                bot_list.append([len(bot_list) + 1, "", "", ""])
            else:
                bot_list.append(
                    [len(bot_list) + 1, bot.name, str(int(bot.current_hp)) + "/" + str(int(bot.max_hp)) + "HP"])
        print(tabulate(bot_list))

    def show_discard(self, class_name=Card):
        cards = []
        card_list = []
        for card in self.discard:
            if isinstance(card, class_name):
                card_formatted = card.listify()
                card_formatted.insert(0, str(len(card_list) + 1))
                card_list.append(card_formatted)
                cards.append(card)
        print(tabulate(card_list))
        return cards

    def show_stats(self):
        print(self.name + ' | Resource: ' + self.resource + ' | HP: ' + str(self.hp) + ' | PP: ' + str(
            self.pp) + ' | Cards: ' + str(len(self.hand)))

