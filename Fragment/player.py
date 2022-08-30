from tabulate import tabulate
from random import randint, shuffle
from card import *
from resourcesHandler import *
import abilities as ab
import numpy as np

blank_frame = Frame("Bot", "None", 0, 0, "None", "None", "None")
# Action costs
_start_pp = 0
_start_hp = 20
_draw_cost = 1
_resource_swap_cost = 1
_refresh_cost = 2
_move_cost = 1

# Ability values
_default_pp_gained = 2
_default_hp_gained = 2
_special_pp_gained = 1


class Player:

    def __init__(self, name: str, resource: str, deck, action_list, ability_list, ai=False, strategy=[1, 1, 1, 1, 1, 1]):
        self.name = name
        self.resource = resource
        self.hp = _start_hp
        self.deck = deck
        self.bots = []
        for i in range(4):
            self.bots.append(Bot(Frame("Bot", "None", 0, 0, "None", "None", "None"), i))
        self.hand = []
        self.discard = []
        self.pp = _start_pp
        self.ai = ai
        self.strategy = strategy
        self.draw_cost = _draw_cost
        self.resource_swap_cost = _resource_swap_cost
        self.refresh_cost = _refresh_cost
        self.move_cost = _move_cost
        self.default_pp_gained = _default_pp_gained
        self.default_hp_gained = _default_hp_gained
        self.special_pp_gained = _special_pp_gained
        self.actions = []
        self.def_bonus = 0
        self.action_list = action_list
        self.ability_list = ability_list

    def count_cards(self):
        card_count = [0, 0, 0, 0]
        for card in self.hand:
            if isinstance(card, Frame):
                card_count[0] += 1
            if isinstance(card, Generator):
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
        headers = ["ID", "Name", "Type", "Cost", "HP", "Ability 1", "Ability 2"]
        card_list = []
        for card in self.hand:
            if isinstance(card, class_name):
                card_formatted = card.listify(discount)
                card_formatted.insert(0, str(len(card_list) + 1))
                card_list.append(card_formatted)
                cards.append(card)
        print(tabulate(card_list, headers=headers))
        return cards

    def listify_bots(self):
        bot_list = []
        for bot in self.bots:
            if bot.isblank():
                bot_list.append([" ", " ", " "])
            else:
                abs = ', '.join(bot.abilities + bot.actions)
                bot_list.append([bot.name, str(int(bot.current_hp)) + "/" + str(int(bot.max_hp)) + "HP", abs])
        bot_list = np.array(bot_list).T.tolist()
        return bot_list

    def show_bots(self):
        cards = []
        bot_list = []
        for bot in self.bots:
            if bot.isblank():
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

    # TODO: Refactor abilities to integrate this code
    def gen_pp(self, bot_num: int, pp_gain: int, source: str, show=False):
        if self.bots[bot_num].stunned:
            return 0
        self.pp += pp_gain
        if show and pp_gain > 0:
            print(self.name, "'s bot", self.bots[bot_num].name, 'generated', pp_gain, 'PP using', source)
        return 1

    def draw(self):
        self.hand.append(self.deck.pop())
