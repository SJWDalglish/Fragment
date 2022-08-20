import pandas as pd
import numpy as np
from random import randint, shuffle
from tabulate import tabulate
import datetime

types = ["Acquire", "Augment", "Consume", "Convert", "Cultivate", "Preserve"]
resource_types = ["Biomass", "Power Cell", "Fossil Fuel", "Radioactive Material", "Weather Event"]
ap_per_turn = 3
num_resources = 6
hand_start_size = 6
hand_draw_size = 2
p1_start_ap = 0
p2_start_ap = 2
num_generators = 3
num_frames = 3
num_parts = 1
draw_cost = 1
resource_swap_cost = 1
resource_refresh_cost = 2
pp_gained = 2
special_pp_gained = 1


class Card(object):
    def __init__(self, name: str, type: str, cost: int, hp: int, pp: int, ability: str):
        self.name = name
        self.type = type
        self.cost = cost
        self.hp = hp
        self.pp = pp
        self.ability = ability

    def display(self):
        print("\n------\nGenerator: " + self.name)
        print("Type: " + self.type)
        print("Cost: " + str(self.cost))
        print("HP: " + str(self.hp))
        print("PP: " + str(self.pp))
        print("Ability: " + self.ability)
        print("------")

    def listify(self):
        return [self.name, type(self).__name__, str(self.cost) + "AP", str(self.hp) + "HP",
                str(self.pp) + "PP"]  # Removed self.ability


class Generator(Card):
    def __init__(self, name: str, type: str, cost: int, pp: int, ability: str):
        hp = 0
        super().__init__(name, type, cost, hp, pp, ability)


class Frame(Card):
    def __init__(self, name: str, type: str, cost: int, hp: int, ability: str):
        pp = 0
        super().__init__(name, type, cost, hp, pp, ability)


class Part(Card):
    def __init__(self, name: str, cost: int, hp: int, pp: int, ability: str):
        type = "None"
        super().__init__(name, type, cost, hp, pp, ability)


class Bot:
    def __init__(self, gen: Generator, frame: Frame, position=None):
        if gen.type != frame.type:
            print("Mismatched types. Bot not Built.")
        self.name = gen.name + frame.name
        self.type = gen.type
        self.current_hp = frame.hp
        self.max_hp = frame.hp
        self.pp = gen.pp
        self.abilities = [gen.ability, frame.ability]
        self.components = [gen, frame]
        self.resources = ['Power Cell']
        if self.type == 'Augment':
            self.resources.append('Radioactive Material')
        elif self.type == 'Consume':
            self.resources.append('Fossil Fuel')
        elif self.type == "Convert":
            self.resources.append('Weather Event')
        elif self.type == "Cultivate":
            self.resources.append('Biomass')
        self.position = position

    def displayName(self):
        print(self.name)

    def display(self):
        print("\n------\nBot: " + self.name)
        # print("Type: " + self.type)
        print("HP: " + str(self.current_hp) + "/" + str(self.max_hp))
        print("PP: " + str(self.pp))
        print("Effects:")
        for i in range(len(self.abilities)):
            print("   [" + str(i) + "] " + self.abilities[i])
        print("------")

    def displayActions(self):
        for i in range(len(self.abilities)):
            print("Ability " + str(i + 1) + ": " + self.abilities[i])

    def dmg(self, dmg: int):
        self.current_hp -= dmg

    def gen(self, pow: int):
        self.pp += pow

    def upgrade(self, part: Part):
        numComponents = len(self.components)
        self.components.insert(numComponents - 1, part)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        self.max_hp += part.hp
        self.current_hp += part.hp
        self.pp += part.pp
        self.abilities.append(part.ability)

    def stringify(self):
        return self.name + "\nHP: " + str(self.current_hp) + "/" + str(self.max_hp) + "\nPP: " + str(self.pp)

    def isblank(self):
        if self.name == 'BlankBot':
            return True
        return False


class Bot2:
    def __init__(self, frame: Frame, position=None):
        self.name = frame.name
        self.type = None
        self.current_hp = frame.hp
        self.max_hp = frame.hp
        self.pp = 0
        self.abilities = [frame.ability]
        self.components = [frame]
        self.position = position

    def power(self, gen: Generator):
        self.type = gen.type
        self.pp = gen.pp
        self.abilities.append(gen.ability)
        self.components.insert(0,gen)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        self.resources = ['Power Cell']
        if self.type == 'Augment':
            self.resources.append('Radioactive Material')
        elif self.type == 'Consume':
            self.resources.append('Fossil Fuel')
        elif self.type == "Convert":
            self.resources.append('Weather Event')
        elif self.type == "Cultivate":
            self.resources.append('Biomass')

    def displayName(self):
        print(self.name)

    def display(self):
        print("\n------\nBot: " + self.name)
        # print("Type: " + self.type)
        print("HP: " + str(self.current_hp) + "/" + str(self.max_hp))
        print("PP: " + str(self.pp))
        print("Effects:")
        for i in range(len(self.abilities)):
            print("   [" + str(i) + "] " + self.abilities[i])
        print("------")

    def displayActions(self):
        for i in range(len(self.abilities)):
            print("Ability " + str(i + 1) + ": " + self.abilities[i])

    def dmg(self, dmg: int):
        self.current_hp -= dmg

    def gen(self, pow: int):
        self.pp += pow

    def upgrade(self, part: Part):
        numComponents = len(self.components)
        self.components.insert(numComponents - 1, part)
        self.name = ""
        for comps in self.components:
            self.name += comps.name
        self.max_hp += part.hp
        self.current_hp += part.hp
        self.pp += part.pp
        self.abilities.append(part.ability)

    def stringify(self):
        return self.name + "\nHP: " + str(self.current_hp) + "/" + str(self.max_hp) + "\nPP: " + str(self.pp)

    def isblank(self):
        if self.name == 'BlankBot':
            return True
        return False


blank_bot = Bot(Generator("Blank", "None", 0, 0, "None"), Frame("Bot", "None", 0, 0, "None"))
blank_bot2 = Bot2(Frame("Bot", "None", 0, 0, "None"))


class Player:
    def __init__(self, name: str, type: str, deck, ai=False, strategy=[1, 1, 1, 1, 1, 1]):
        self.name = name
        self.type = type
        self.hp = 20
        self.deck = deck
        self.bots = [blank_bot, blank_bot, blank_bot, blank_bot]
        self.hand = []
        self.ap = 0
        self.ai = ai
        self.strategy = strategy

    def get_resource_types(self):
        output = ['Power Cell']
        if self.type == 'Augment':
            output.append('Radioactive Material')
        elif self.type == 'Consume':
            output.append('Fossil Fuel')
        elif self.type == "Convert":
            output.append('Weather Event')
        elif self.type == "Cultivate":
            output.append('Biomass')
        return output

    def draw(self, show=False):
        card = self.deck.pop()
        self.hand.append(card)
        self.ap -= draw_cost
        if show:
            print(self.name + ' draws card ' + card.name)
        if self.type == 'Preserve':
            for i in range(4):
                self.bots[i].pp += special_pp_gained
        return card

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

    def show_hand(self, class_name=Card):
        cards = []
        card_list = []
        for card in self.hand:
            if isinstance(card, class_name):
                card_formatted = card.listify()
                card_formatted.insert(0, len(card_list) + 1)
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
                    [len(bot_list) + 1, bot.name, str(int(bot.current_hp)) + "/" + str(int(bot.max_hp)) + "HP",
                     str(int(bot.pp)) + "PP"])
        print(tabulate(bot_list))

    def show_stats(self):
        print(self.name + ' | Type: ' + self.type + ' | HP: ' + str(self.hp) + ' | AP: ' + str(
            self.ap) + ' | Cards: ' + str(
            len(self.hand)))

    def ai_build(self, possible_combos, show=False):
        choice = randint(0, len(possible_combos) - 1)
        bot_num_selected = randint(0, 3)
        gen_selected = possible_combos[choice][0]
        frame_selected = possible_combos[choice][1]
        new_bot = Bot(gen_selected, frame_selected, bot_num_selected + 1)

        if show:
            print(self.name + " is building a bot using " + gen_selected.name + ' and ' + frame_selected.name)
        self.hand.remove(gen_selected)
        self.hand.remove(frame_selected)
        self.ap -= gen_selected.cost + frame_selected.cost
        self.bots[bot_num_selected] = new_bot
        return new_bot

    def ai_build2(self, possible_combos, show=False):
        choice = randint(0, len(possible_combos) - 1)
        bot_num_selected = randint(0, 3)
        frame_selected = possible_combos[choice][1]
        new_bot = Bot2(frame_selected, bot_num_selected + 1)

        if show:
            print(self.name + " is building a bot using " + frame_selected.name)
        self.hand.remove(frame_selected)
        self.ap -= frame_selected.cost
        self.bots[bot_num_selected] = new_bot
        return new_bot

    def build(self):
        # Handle ai elsewhere
        if self.ai:
            self.ai_build()
            return 1

        # Select a generator
        gen_cards = self.show_hand(Generator)
        if len(gen_cards) == 0:
            print('No generators in hand!')
            return 0
        gen_selected = select_card_list(gen_cards, self, 'Select a generator ')
        if gen_selected is None:
            return 0

        # Select a frame
        frame_cards = self.show_hand(Frame)
        if len(frame_cards) == 0:
            print('No generators in hand!')
            return 0
        frame_selected = select_card_list(frame_cards, self, 'Select a generator ', gen_selected.cost)
        if frame_selected is None:
            return 0

        # Select a bot location
        self.show_bots()
        while True:
            bot_num_selected = select_bot_list(self, 'Select a build location ')
            if bot_num_selected is None:
                return 0
            if not self.bots[int(bot_num_selected) - 1].isblank():
                answer = ''
                while True:
                    answer = input('Are you sure you want to replace this bot? Y/N')
                    if answer == "y" or answer == "Y":
                        break
                    elif answer == "n" or answer == "N":
                        break
                    else:
                        print('Invalid response!')
                if answer == "y" or answer == "Y":
                    break
                elif answer == "n" or answer == "N":
                    continue
            break

        # Clean up hand, minus ap, add bot
        new_bot = Bot(gen_selected, frame_selected, int(bot_num_selected))
        self.hand.remove(gen_selected)
        self.hand.remove(frame_selected)
        self.ap -= gen_selected.cost + frame_selected.cost
        self.bots[int(bot_num_selected) - 1] = new_bot
        return 1

    def build2(self):
        # Handle ai elsewhere
        if self.ai:
            self.ai_build2()
            return 1

        # Select a frame
        frame_cards = self.show_hand(Frame)
        if len(frame_cards) == 0:
            print('No generators in hand!')
            return 0
        frame_selected = select_card_list(frame_cards, self, 'Select a frame ')
        if frame_selected is None:
            return 0

        # Select a bot location
        self.show_bots()
        while True:
            bot_num_selected = select_bot_list(self, 'Select a build location ')
            if bot_num_selected is None:
                return 0
            if not self.bots[int(bot_num_selected) - 1].isblank():
                answer = ''
                while True:
                    answer = input('Are you sure you want to replace this bot? Y/N')
                    if answer == "y" or answer == "Y":
                        break
                    elif answer == "n" or answer == "N":
                        break
                    else:
                        print('Invalid response!')
                if answer == "y" or answer == "Y":
                    break
                elif answer == "n" or answer == "N":
                    continue
            break

        # Clean up hand, minus ap, add bot
        new_bot = Bot2(frame_selected, int(bot_num_selected))
        self.hand.remove(frame_selected)
        self.ap -= frame_selected.cost
        self.bots[int(bot_num_selected) - 1] = new_bot
        return 1

    def power(self):
        # Handle ai elsewhere
        if self.ai:
            self.ai_power()
            return 1

        # Select a bot location
        self.show_bots()
        while True:
            bot_selected = select_bot_list(self, 'Select a bot to upgrade ')
            if bot_selected is None:
                return 0
            if self.bots[int(bot_selected) - 1].isblank():
                print('No bot selected.')
                continue
            break

        # Select a generator
        gen_cards = self.show_hand(Generator)
        if len(gen_cards) == 0:
            print('No generators in hand!')
            return 0
        gen_selected = select_card_list(gen_cards, self, 'Select a generator ')
        if gen_selected is None:
            return 0

        # Clean up
        self.bots[int(bot_selected) - 1].power(gen_selected)
        self.ap -= gen_selected.cost
        self.hand.remove(gen_selected)
        return 1

    def ai_upgrade(self, possible_upgrades, show=False):
        upgrade_bots = []
        for bot in self.bots:
            if not bot.isblank():
                upgrade_bots.append(bot)
        bot_choice = randint(0, len(upgrade_bots) - 1)
        part_choice = randint(0, len(possible_upgrades) - 1)
        part_selected = possible_upgrades[part_choice]

        if show:
            print(self.name + " is upgrading " + upgrade_bots[bot_choice].name + ' with ' + part_selected.name)
        upgrade_bots[bot_choice].upgrade(part_selected)
        self.ap -= part_selected.cost
        self.hand.remove(part_selected)

        return [upgrade_bots[bot_choice], part_selected]

    def upgrade(self):
        # Select a bot location
        self.show_bots()
        while True:
            bot_selected = select_bot_list(self, 'Select a bot to upgrade ')
            if bot_selected is None:
                return 0
            if self.bots[int(bot_selected) - 1].isblank():
                print('No bot selected.')
                continue
            break

        # Select a part
        part_cards = self.show_hand(Part)
        if len(part_cards) == 0:
            print('No generators in hand!')
            return 0
        part_selected = select_card_list(part_cards, self, 'Select a part ')
        if part_selected is None:
            return 0

        # Clean up
        self.bots[int(bot_selected) - 1].upgrade(part_selected)
        self.ap -= part_selected.cost
        self.hand.remove(part_selected)

    def generate_pp(self, opponent, resource_handler, show=False):
        for i in range(4):
            bot = self.bots[i]
            if not bot.isblank():
                if bot.resources.count(resource_handler.pile[i]) > 0:
                    self.bots[i].pp += pp_gained
                    if show:
                        print(self.name + "'s bot " + self.bots[i].name + ' regained ' + str(
                            pp_gained) + 'pp using adjacent resource.')
                    if opponent.bots[i].type == "Acquire":
                        opponent.bots[i].pp += special_pp_gained
                        if show:
                            print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                                special_pp_gained) + 'pp from opposing bot.')
                if bot.type == 'Augment':
                    self.bots[i].pp += special_pp_gained * (len(bot.components) - 2)
                    if show:
                        print(self.name + "'s bot " + self.bots[i].name + ' regained ' + str(
                            special_pp_gained * (len(bot.components) - 2)) + 'pp using repurposed hardware.')
                    if opponent.bots[i].type == "Acquire":
                        opponent.bots[i].pp += special_pp_gained
                        if show:
                            print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                                special_pp_gained) + 'pp from opposing bot.')
                if bot.type == 'Convert':
                    for j in range(4):
                        if (j != i) and (resource_handler.pile[j] == 'Weather Event'):
                            self.bots[i].pp += special_pp_gained
                            if show:
                                print(self.name + "'s bot " + self.bots[i].name + ' regained ' + str(
                                    special_pp_gained) + 'pp due to inclement weather.')
                            if opponent.bots[i].type == "Acquire":
                                opponent.bots[i].pp += special_pp_gained
                                if show:
                                    print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                                        special_pp_gained) + 'pp from opposing bot.')
                if bot.type == 'Cultivate':
                    for j in range(4):
                        if (j != i) and (self.bots[j].type == 'Cultivate'):
                            self.bots[i].pp += special_pp_gained
                            if show:
                                print(self.name + "'s bot " + self.bots[i].name + ' regained ' + str(
                                    special_pp_gained) + 'pp due to a thriving ecosystem.')
                            if opponent.bots[i].type == "Acquire":
                                opponent.bots[i].pp += special_pp_gained
                                if show:
                                    print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                                        special_pp_gained) + 'pp from opposing bot.')

    def swap_resource(self, resource_handler):
        resource_pile = ""
        for i in range(4):
            resource_pile += "\n[" + str(i) + "]" + resource_handler.pile[i]
        print(resource_pile)
        while True:
            num_choice = input('Select a resource to swap or press [x] to cancel.')
            if num_choice == 'x':
                return 0
            if num_choice in [str(x) for x in range(4)]:
                old_resource = resource_handler.pile[int(num_choice)]
                resource_handler.pile[int(num_choice)] = resource_handler.deck.pop()
                resource_handler.deck.insert(0, old_resource)
                self.ap -= resource_swap_cost
                if self.type == 'Consume' and old_resource == 'Fossil Fuel':
                    for bot in self.bots:
                        if not bot.isblank():
                            bot.pp += special_pp_gained * 4
                break

    def ai_swap_resource(self, rh, show=False, possible_swaps=[]):
        if possible_swaps == []:
            good_resources = self.get_resource_types()
            for i in range(4):
                if rh.pile[i] not in good_resources:
                    possible_swaps.append(i)
        num_choice = randint(0, len(possible_swaps) - 1)
        old_resource = rh.pile[possible_swaps[num_choice]]
        new_resource = rh.deck.pop()
        rh.pile[possible_swaps[num_choice]] = new_resource
        rh.deck.insert(0, old_resource)
        self.ap -= resource_swap_cost
        if show:
            print(self.name + ' is swapping resource ' + old_resource + ' for ' + new_resource)
        return [num_choice, old_resource, new_resource]

    def refresh_resources(self, rh, show=False):
        rh.deck = rh.pile + rh.deck
        for i in range(4):
            if self.type == 'Consume' and rh.pile[i] == 'Fossil Fuel':
                for bot in self.bots:
                    if not bot.isblank():
                        bot.pp += special_pp_gained * 4
        for i in range(4):
            rh.pile[i] = rh.deck.pop()
        self.ap -= resource_refresh_cost
        if show:
            print(self.name + ' is refreshing all resources')

    def attack(self, opponent, show=False):
        for i in range(4):
            if self.bots[i].isblank():
                continue

            # Attack opponent directly
            elif opponent.bots[i].isblank():
                dmg = self.bots[i].pp
                opponent.hp -= dmg
                self.bots[i].pp = 0
                if show:
                    print(self.name + ' uses ' + self.bots[i].name + ' to attack ' + opponent.name + ' for ' + str(
                        dmg) + ' damage, leaving ' + str(opponent.hp) + 'hp remaining')

                # Reallocate
                reallocate_amount = min(opponent.ap, self.bots[i].abilities.count('Reallocate'))
                opponent.ap -= reallocate_amount
                self.bots[i].pp += reallocate_amount
                if show and 'Reallocate' in self.bots[i].abilities:
                    print(self.name + ' uses ' + self.bots[i].name + ' to Reallocate ' + opponent.name + "'s bot" +
                          opponent.bots[target].name + "resources")

            # Attack opposing bot
            else:
                attack_amount = min(self.bots[i].pp, opponent.bots[i].current_hp)
                attack_amount -= opponent.bots[i].abilities.count('Shield')
                opponent.bots[i].current_hp -= attack_amount
                self.bots[i].pp -= attack_amount
                if show:
                    print(self.name + ' uses ' + self.bots[i].name + ' to attack ' + opponent.name + "'s bot, " +
                          opponent.bots[i].name + ', for ' + str(attack_amount) + ' damage, leaving ' + str(
                        opponent.bots[i].current_hp) + 'hp remaining')

                target = randint(0, 3)
                if 'Hurricane' in self.bots[i].abilities:
                    swap_bot = opponent.bots[target]
                    opponent.bots[target] = opponent.bots[i]
                    opponent.bots[i] = swap_bot

            # Handle abilities
            target = randint(0, 3)

            # Scorch
            opponent.bots[target].current_hp -= self.bots[i].abilities.count('Scorch')
            if show and 'Scorch' in self.bots[i].abilities and not opponent.bots[target].isblank():
                print(self.name + ' uses ' + self.bots[i].name + ' to Scorch ' + opponent.name + "'s bot " +
                      opponent.bots[target].name + ' for ' + str(
                    self.bots[i].abilities.count('Scorch')) + ' damage, leaving ' + str(
                    opponent.bots[target].current_hp) + 'hp remaining')

            # Pack
            self.bots[target].current_hp += 2 * self.bots[i].abilities.count('Pollinate')
            if show and 'Pack' in self.bots[i].abilities and not self.bots[target].isblank():
                print(self.name + ' uses ' + self.bots[i].name + ' to Heal ' + self.bots[target].name + ' for ' + str(
                    self.bots[i].abilities.count('Pollinate') * 2) + 'hp to ' + str(
                    self.bots[target].current_hp) + 'hp')

            # Mutate
            self.bots[target].pp += self.bots[i].abilities.count('Mutate')
            if show and 'Mutate' in self.bots[i].abilities and not self.bots[target].isblank():
                print(self.name + ' uses ' + self.bots[i].name + ' to Mutate ' + self.bots[target].name + ' for ' + str(
                    self.bots[i].abilities.count('Mutate')) + 'pp to ' + str(self.bots[target].pp) + 'pp')

        # Clean up broken bots
        for i in range(4):
            if opponent.bots[i].current_hp <= 0:
                bot = opponent.bots[i]
                opponent.deck = bot.components + opponent.deck
                opponent.bots[i] = blank_bot


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


def init_decks():
    while True:
        player_game_style = input(
            "How do you want to play?\n[1] Against an AI\n[2] Against myself\n[3] Watch the AI play")
        if not (["1", "2", "3"].count(player_game_style) > 0):
            print("Not an available option!")
            continue
        if player_game_style in ["1", "2", "3"]:
            break

    if player_game_style == "1":
        while True:
            player_type_num = input("Choose a deck!"
                                    "\n[1] Acquire"
                                    "\n[2] Augment"
                                    "\n[3] Consume"
                                    "\n[4] Convert"
                                    "\n[5] Cultivate"
                                    "\n[6] Preserve"
                                    "\n[7] Show Details"
                                    "\n[8] Exit")
            if not (["1", "2", "3", "4", "5", "6", "7", "8"].count(player_type_num) > 0):
                print("Not an available option!")
                continue
            if player_type_num in ["1", "2", "3", "4", "5", "6"]:
                player_type = types[int(player_type_num) - 1]
                break
            if player_type_num == "7":
                print("Acquire: Steal opponents' PP and HP."
                      "\nAugment: Gain PP from attached parts."
                      "\nConsume: Burn resources for a quick PP gain."
                      "\nConvert: Gain PP from all weather events."
                      "\nCultivate: Gain PP from all friendly bots."
                      "\nPreserve: Spend AP to charge bots.")
            if player_type_num == "8":
                return None, None, None
        opponent_type = types[randint(0, 5)]

    if player_game_style == "2":
        while True:
            player_type_num = input("Choose a deck!"
                                    "\n[1] Acquire"
                                    "\n[2] Augment"
                                    "\n[3] Consume"
                                    "\n[4] Convert"
                                    "\n[5] Cultivate"
                                    "\n[6] Preserve"
                                    "\n[7] Show Details"
                                    "\n[8] Exit")
            if not (["1", "2", "3", "4", "5", "6", "7", "8"].count(player_type_num) > 0):
                print("Not an available option!")
                continue
            if player_type_num in ["1", "2", "3", "4", "5", "6"]:
                player_type = types[int(player_type_num) - 1]
                break
            if player_type_num == "7":
                print("Acquire: Steal opponents' PP and HP."
                      "\nAugment: Gain PP from attached parts."
                      "\nConsume: Burn resources for a quick PP gain."
                      "\nConvert: Gain PP from all weather events."
                      "\nCultivate: Gain PP from all friendly bots."
                      "\nPreserve: Spend AP to charge bots.")
            if player_type_num == "8":
                return None, None, None
        while True:
            opponent_type_num = input("Choose a deck for your opponent!"
                                      "\n[1] Acquire"
                                      "\n[2] Augment"
                                      "\n[3] Consume"
                                      "\n[4] Convert"
                                      "\n[5] Cultivate"
                                      "\n[6] Preserve"
                                      "\n[7] Show Details"
                                      "\n[8] Exit")
            if not (["1", "2", "3", "4", "5", "6", "7", "8"].count(opponent_type_num) > 0):
                print("Not an available option!")
                continue
            if opponent_type_num in ["1", "2", "3", "4", "5", "6"]:
                opponent_type = types[int(opponent_type_num) - 1]
                break
            if opponent_type_num == "7":
                print("Acquire: Steal opponents' PP and HP."
                      "\nAugment: Gain PP from attached parts."
                      "\nConsume: Burn resources for a quick PP gain."
                      "\nConvert: Gain PP from all weather events."
                      "\nCultivate: Gain PP from all friendly bots."
                      "\nPreserve: Spend AP to charge bots.")
            if opponent_type_num == "8":
                return None, None, None

    if player_game_style == "3":
        player_type = types[randint(0, 5)]
        opponent_type = types[randint(0, 5)]

    player_deck = []
    opponent_deck = []

    [generators, frames, parts] = prep_cards()

    for card in generators:
        if card.type == player_type:
            player_deck.extend(num_generators * list([card]))
        if card.type == opponent_type:
            opponent_deck.extend(num_generators * list([card]))
    for card in frames:
        if card.type == player_type:
            player_deck.extend(num_frames * list([card]))
        if card.type == opponent_type:
            opponent_deck.extend(num_frames * list([card]))
    for card in parts:
        player_deck.extend(num_parts * list([card]))
        opponent_deck.extend(num_parts * list([card]))

    shuffle(player_deck)
    shuffle(opponent_deck)
    player_ai = player_game_style == "3"
    opponent_ai = (player_game_style == "1" or player_game_style == "3")

    player = Player("Player 1", player_type, player_deck, player_ai)
    opponent = Player("Player 2", opponent_type, opponent_deck, opponent_ai)

    resource_handler = ResourceHandler()

    return player, opponent, resource_handler, player_ai


def init_game():
    player1, player2, resource_handler, show = init_decks()
    if player1 is None:
        return None
    for i in range(hand_start_size):
        player1.draw()
        player2.draw()
    turn = randint(0, 1)
    if turn == 0:
        player1.ap = p1_start_ap
        player2.ap = p2_start_ap
    else:
        player1.ap = p2_start_ap
        player2.ap = p1_start_ap
    winner = game_manager(turn, player1, player2, resource_handler, show)
    if winner == 1:
        print(player1.name + ' wins!!')
    elif winner == 2:
        print(player2.name + ' wins!!')
    else:
        return 0


def init_game2():
    player1, player2, resource_handler, show = init_decks()
    if player1 is None:
        return None
    for i in range(hand_start_size):
        player1.draw()
        player2.draw()
    turn = randint(0, 1)
    if turn == 0:
        player1.ap = p1_start_ap
        player2.ap = p2_start_ap
    else:
        player1.ap = p2_start_ap
        player2.ap = p1_start_ap
    winner = game_manager2(turn, player1, player2, resource_handler, show)
    if winner == 1:
        print(player1.name + ' wins!!')
    elif winner == 2:
        print(player2.name + ' wins!!')
    else:
        return 0


def game_manager(turn, player1, player2, resource_handler, show=False):
    while player1.hp > 0 and player2.hp > 0:
        if turn == 0:
            exit_status = take_turn(player1, player2, resource_handler, show)
            if exit_status == 0:
                return 0
            turn = 1
        else:
            exit_status = take_turn(player2, player1, resource_handler, show)
            if exit_status == 0:
                return 0
            turn = 0
    if player1.hp > 0:
        return 1
    else:
        return 2


def game_manager2(turn, player1, player2, resource_handler, show=False):
    while player1.hp > 0 and player2.hp > 0:
        if turn == 0:
            exit_status = take_turn2(player1, player2, resource_handler, show)
            if exit_status == 0:
                return 0
            turn = 1
        else:
            exit_status = take_turn2(player2, player1, resource_handler, show)
            if exit_status == 0:
                return 0
            turn = 0
    if player1.hp > 0:
        return 1
    else:
        return 2


def take_turn(player, opponent, resource_handler, show=False, log=[]):
    player.generate_pp(opponent, resource_handler, True)  # Generate PP for bots according to associated resources
    player.ap += ap_per_turn  # Update AP
    for i in range(hand_draw_size):
        player.hand.append(player.deck.pop())  # Draw a card

    output = 1

    if player.ai:
        output = take_turn_ai(player, opponent, resource_handler, show)

    if not player.ai:
        output = take_turn_player(player, opponent, resource_handler)

    player.attack(opponent, True)
    return output


def take_turn2(player, opponent, resource_handler, show=False, log=[]):
    player.generate_pp(opponent, resource_handler, True)  # Generate PP for bots according to associated resources
    player.ap += ap_per_turn  # Update AP
    for i in range(hand_draw_size):
        player.hand.append(player.deck.pop())  # Draw a card

    output = 1

    if player.ai:
        output = take_turn_ai2(player, opponent, resource_handler, show)

    if not player.ai:
        output = take_turn_player2(player, opponent, resource_handler)

    player.attack(opponent, True)
    return output


def take_turn_ai(player, opponent, resource_handler, show=False):
    while True:
        available_choices = []  # Used to track choices available to the player
        card_count = player.count_cards()
        gen_cards = player.get_hand(Generator)
        frame_cards = player.get_hand(Frame)
        part_cards = player.get_hand(Part)

        possible_combos = []  # Check if a bot can be built
        if card_count[0] > 0 and card_count[1] > 0:
            for card1 in gen_cards:
                for card2 in frame_cards:
                    if card1.cost + card2.cost <= player.ap:
                        possible_combos.append([card1, card2])
        if len(possible_combos) > 0:
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')

        possible_upgrades = []  # Check if a bot can be upgraded
        if card_count[2] > 0 and card_count[3] > 0:
            for card in part_cards:
                if card.cost <= player.ap:
                    possible_upgrades.append(card)
        if len(possible_upgrades) > 0:
            available_choices.append('Upgrade a bot')
            available_choices.append('Upgrade a bot')
            available_choices.append('Upgrade a bot')

        possible_swaps = []
        good_resources = player.get_resource_types()
        for resource in resource_handler.pile:
            if resource not in good_resources:
                possible_swaps.append(resource)

        if player.ap >= resource_swap_cost and len(possible_swaps) > 0:
            available_choices.append('Swap a resource')
            available_choices.append('Swap a resource')
        if player.ap >= resource_refresh_cost and len(possible_swaps) == 4:
            available_choices.append('Refresh all resources')
        if player.ap >= draw_cost:
            available_choices.append('Draw a card')
            available_choices.append('Draw a card')
        # if player.ap >= ability_cost: # to add later
        available_choices.append('End Turn')

        num_choice = randint(0, len(available_choices) - 1)
        choice = available_choices[num_choice]

        if choice == 'Build a bot':
            bot_built = player.ai_build(possible_combos, show)
        elif choice == 'Upgrade a bot':
            [bot_upgraded, part_upgraded] = player.ai_upgrade(possible_upgrades, show)
        elif choice == 'Swap a resource':
            [resource_position, old_resource, new_resource] = player.ai_swap_resource(resource_handler, show)
        elif choice == 'Refresh all resources':
            player.refresh_resources(resource_handler, show)
        elif choice == 'Draw a card':
            card_drawn = player.draw(show)
        elif choice == 'End Turn':
            if show:
                print(player.name + ' ends their turn.')
            break
    return 1


def take_turn_player(player, opponent, resource_handler):
    while True:  # Iterate through choices available during turn
        display_field(player, opponent, resource_handler)
        available_choices = []  # Used to track choices available to the player
        card_count = player.count_cards()
        if card_count[0] > 0 and card_count[1] > 0:
            available_choices.append('Build a bot')
        if card_count[2] > 0 and card_count[3] > 0:
            available_choices.append('Upgrade a bot')
        if player.ap >= resource_swap_cost:
            available_choices.append('Swap a resource')
        if player.ap >= resource_refresh_cost:
            available_choices.append('Refresh all resources')
        if player.ap >= draw_cost:
            available_choices.append('Draw a card')
        # if player.ap >= ability_cost: # to add later
        available_choices.append('End Turn')
        available_choices.append('Exit Game')

        labelled_choices = ["[" + str(i + 1) + "] " + available_choices[i] for i in range(len(available_choices))]
        labelled_choices = '\n'.join(labelled_choices)

        while True:
            num_choice = input(labelled_choices)
            if not num_choice.isdecimal():
                print('Not a valid input.')
                continue
            elif int(num_choice) in [x + 1 for x in range(len(available_choices))]:
                choice = available_choices[int(num_choice) - 1]
                break

        # choice = input('Select an action to take:\n[1] Build a bot\n[2] Upgrade a bot\n[3] Collect a resource\n'
        #                '[4] Refresh resources\n[5] End turn\n[6] Draw a card\n[7] Exit')
        if choice == 'Build a bot':
            player.build()
        elif choice == 'Upgrade a bot':
            player.upgrade()
        elif choice == 'Swap a resource':
            player.swap_resource(resource_handler)
        elif choice == 'Refresh all resources':
            player.refresh_resources(resource_handler)
        elif choice == 'Draw a card':
            player.draw()
        elif choice == 'End Turn':
            break
        elif choice == 'Exit Game':
            return 0
    return 1


def take_turn_ai2(player, opponent, resource_handler, show=False):
    while True:
        available_choices = []  # Used to track choices available to the player
        card_count = player.count_cards()
        gen_cards = player.get_hand(Generator)
        frame_cards = player.get_hand(Frame)
        part_cards = player.get_hand(Part)

        possible_combos = []  # Check if a bot can be built
        if card_count[0] > 0 and card_count[1] > 0:
            for card1 in gen_cards:
                for card2 in frame_cards:
                    if card1.cost + card2.cost <= player.ap:
                        possible_combos.append([card1, card2])
        if len(possible_combos) > 0:
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')

        possible_upgrades = []  # Check if a bot can be upgraded
        if card_count[2] > 0 and card_count[3] > 0:
            for card in part_cards:
                if card.cost <= player.ap:
                    possible_upgrades.append(card)
        if len(possible_upgrades) > 0:
            available_choices.append('Upgrade a bot')
            available_choices.append('Upgrade a bot')
            available_choices.append('Upgrade a bot')

        possible_swaps = []
        good_resources = player.get_resource_types()
        for resource in resource_handler.pile:
            if resource not in good_resources:
                possible_swaps.append(resource)

        if player.ap >= resource_swap_cost and len(possible_swaps) > 0:
            available_choices.append('Swap a resource')
            available_choices.append('Swap a resource')
        if player.ap >= resource_refresh_cost and len(possible_swaps) == 4:
            available_choices.append('Refresh all resources')
        if player.ap >= draw_cost:
            available_choices.append('Draw a card')
            available_choices.append('Draw a card')
        # if player.ap >= ability_cost: # to add later
        available_choices.append('End Turn')

        num_choice = randint(0, len(available_choices) - 1)
        choice = available_choices[num_choice]

        if choice == 'Build a bot':
            bot_built = player.ai_build(possible_combos, show)
        elif choice == 'Upgrade a bot':
            [bot_upgraded, part_upgraded] = player.ai_upgrade(possible_upgrades, show)
        elif choice == 'Swap a resource':
            [resource_position, old_resource, new_resource] = player.ai_swap_resource(resource_handler, show)
        elif choice == 'Refresh all resources':
            player.refresh_resources(resource_handler, show)
        elif choice == 'Draw a card':
            card_drawn = player.draw(show)
        elif choice == 'End Turn':
            if show:
                print(player.name + ' ends their turn.')
            break
    return 1


def take_turn_player2(player, opponent, resource_handler):
    while True:  # Iterate through choices available during turn
        display_field(player, opponent, resource_handler)
        available_choices = []  # Used to track choices available to the player
        card_count = player.count_cards()
        if card_count[0] > 0:
            available_choices.append('Build a bot')
        if card_count[1] > 0 and card_count[3] > 0:
            available_choices.append('Power a bot')
        if card_count[2] > 0 and card_count[3] > 0:
            available_choices.append('Upgrade a bot')
        if player.ap >= resource_swap_cost:
            available_choices.append('Swap a resource')
        if player.ap >= resource_refresh_cost:
            available_choices.append('Refresh all resources')
        if player.ap >= draw_cost:
            available_choices.append('Draw a card')
        # if player.ap >= ability_cost: # to add later
        available_choices.append('End Turn')
        available_choices.append('Exit Game')

        labelled_choices = ["[" + str(i + 1) + "] " + available_choices[i] for i in range(len(available_choices))]
        labelled_choices = '\n'.join(labelled_choices)

        while True:
            num_choice = input(labelled_choices)
            if not num_choice.isdecimal():
                print('Not a valid input.')
                continue
            elif int(num_choice) in [x + 1 for x in range(len(available_choices))]:
                choice = available_choices[int(num_choice) - 1]
                break

        # choice = input('Select an action to take:\n[1] Build a bot\n[2] Upgrade a bot\n[3] Collect a resource\n'
        #                '[4] Refresh resources\n[5] End turn\n[6] Draw a card\n[7] Exit')
        if choice == 'Build a bot':
            player.build2()
        elif choice == 'Power a bot':
            player.power()
        elif choice == 'Upgrade a bot':
            player.upgrade()
        elif choice == 'Swap a resource':
            player.swap_resource(resource_handler)
        elif choice == 'Refresh all resources':
            player.refresh_resources(resource_handler)
        elif choice == 'Draw a card':
            player.draw()
        elif choice == 'End Turn':
            break
        elif choice == 'Exit Game':
            return 0
    return 1


def prep_cards():
    # abilities = pd.read_csv('Fragment 1.0 CSV Files/Abilities.csv')
    frames = pd.read_csv('Fragment 1.0 CSV Files/Frames.csv')
    generators = pd.read_csv('Fragment 1.0 CSV Files/Generators.csv')
    parts = pd.read_csv('Fragment 1.0 CSV Files/Parts.csv')

    frame_list = []
    for index, row in frames.iterrows():
        frame_list.append(Frame(row['Name'], row['Type'], row['Cost'], row['HP'], row['Ability']))

    generator_list = []
    for index, row in generators.iterrows():
        generator_list.append(Generator(row['Name'], row['Type'], row['Cost'], row['PP'], row['Ability']))

    part_list = []
    for index, row in parts.iterrows():
        part_list.append(Part(row['Name'], row['Cost'], row['HP'], row['PP'], row['Ability']))

    return [frame_list, generator_list, part_list]


def display_field(player: Player, opponent: Player, resource_handler: ResourceHandler):
    print('\n' + ('+' * 50) + '\n')
    opponent.show_stats()
    opponent.show_bots()
    resource_handler.show_pile()
    player.show_bots()
    player.show_stats()
    player.show_hand()
    print('\n' + ('+' * 50) + '\n')


def select_card_list(card_list: [Card], player: Player, select_text: str, constraint=0):
    card_selected = None
    while True:
        num_selected = input(select_text + 'or press [x] to cancel.')
        if num_selected == 'x':
            return None
        elif not num_selected.isdecimal():
            print('Not a valid input.')
            continue
        elif int(num_selected) in [x + 1 for x in list(range(len(card_list)))]:
            card_selected = card_list[int(num_selected) - 1]
            if card_selected.cost + constraint > player.ap:
                print("Not enough AP!")
                continue
            return card_selected
        print('Not a valid input.')
        continue
    return None


def select_bot_list(player: Player, select_text: str):
    bot_selected = None
    while True:
        num_selected = input(select_text + 'or press [x] to cancel.')
        if num_selected == 'x':
            return None
        elif not num_selected.isdecimal():
            print('Not a valid input.')
            continue
        elif int(num_selected) in [x + 1 for x in list(range(len(player.bots)))]:
            return num_selected
        print('Not a valid input.')
        continue
    return None


def init_test():
    status_log = ['Game', 'Turn', 'Player', 'Object', 'Position', 'Stat', 'Value']
    activity_log = ['Game', 'Turn', 'Player', 'Action', 'Component1', 'Component2', 'Value']
    win_log = ['Game', 'Turns', 'Player1_Type', 'Player1_Strat', 'Player2_Type', 'Player2_Strat', 'Winner',
               'Starter_Wins']
    log = [[], [], []]
    while True:
        num = input('How many iterations?')
        if num.isdecimal():
            for i in range(int(num)):
                print('[', end='')
                strategy1 = []
                strategy2 = []
                for i in range(5):
                    strategy1.append(randint(1, 50))
                    strategy2.append(randint(1, 50))
                s1total = sum(strategy1)
                s2total = sum(strategy2)
                for i in range(5):
                    strategy1[i] = int(100 * strategy1[i] / s1total)
                    strategy2[i] = int(100 * strategy2[i] / s2total)
                strategy1.append(randint(1, 3))
                strategy2.append(randint(1, 3))
                result = run_test_game(i, log, strategy1, strategy2)
                log[2].append([str(i)] + result)
                print(']')
            now = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
            # pd.DataFrame(log[0],columns=status_log).to_csv('CSV/'+now+'_test_status_log.csv', index=False)
            pd.DataFrame(log[1], columns=activity_log).to_csv('CSV/' + now + '_test_activity_log.csv', index=False)
            pd.DataFrame(log[2], columns=win_log).to_csv('CSV/' + now + '_test_win_log.csv', index=False)
            break
        else:
            print('Please enter an integer.')


def run_test_game(game_num: int, log, strategy1, strategy2):
    [generators, frames, parts] = prep_cards()
    player1_type = types[randint(0, 5)]
    player2_type = types[randint(0, 5)]
    player_deck = []
    opponent_deck = []
    for card in generators:
        if card.type == player1_type:
            player_deck.extend(num_generators * list([card]))
        if card.type == player2_type:
            opponent_deck.extend(num_generators * list([card]))
    for card in frames:
        if card.type == player1_type:
            player_deck.extend(num_frames * list([card]))
        if card.type == player2_type:
            opponent_deck.extend(num_frames * list([card]))
    for card in parts:
        player_deck.extend(num_parts * list([card]))
        opponent_deck.extend(num_parts * list([card]))

    shuffle(player_deck)
    shuffle(opponent_deck)
    p1 = Player("Player 1", player1_type, player_deck, True, strategy1)
    p2 = Player("Player 2", player2_type, opponent_deck, True, strategy2)
    rh = ResourceHandler()

    turn = 0
    p2.ap += 1
    turn_num = 0
    while p1.hp > 0 and p2.hp > 0:
        turn_num += 1
        print('-', end='')
        # log[0].append([game_num, turn_num, p1.name, 'Player', 0, 'hp', p1.hp])
        # log[0].append([game_num, turn_num, p2.name, 'Player', 0, 'hp', p2.hp])
        # for i in range(4):
        #     log[0].append([game_num, turn_num, p1.name, 'Bot', i, 'name', p1.bots[i].name])
        #     log[0].append([game_num, turn_num, p1.name, 'Bot', i, 'hp', p1.bots[i].current_hp])
        #     log[0].append([game_num, turn_num, p1.name, 'Bot', i, 'pp', p1.bots[i].pp])
        #     log[0].append([game_num, turn_num, p2.name, 'Bot', i, 'name', p2.bots[i].name])
        #     log[0].append([game_num, turn_num, p2.name, 'Bot', i, 'hp', p2.bots[i].current_hp])
        #     log[0].append([game_num, turn_num, p2.name, 'Bot', i, 'pp', p2.bots[i].pp])
        #     log[0].append([game_num, turn_num, '', 'Resource', i, 'name', rh.pile[i]])
        if turn == 0:
            exit_status = test_turn(p1, p2, rh, game_num, turn_num, log)
            if exit_status == 0:
                return 0
            turn = 1
        else:
            exit_status = test_turn(p2, p1, rh, game_num, turn_num, log)
            if exit_status == 0:
                return 0
            turn = 0
    if p1.hp > 0:
        return [turn_num, p1.type, p1.strategy, p2.type, p2.strategy, p1.name, True]
    else:
        return [turn_num, p1.type, p1.strategy, p2.type, p2.strategy, p2.name, False]


def test_turn(p: Player, o: Player, rh: ResourceHandler, game_num: int, turn_num: int, log):
    p.ap += ap_per_turn  # Update AP
    p.generate_pp(o, rh)  # Generate PP for bots according to associated resources
    for i in range(hand_draw_size):
        p.hand.append(p.deck.pop())  # Draw a card

    while True:
        available_choices = []  # Used to track choices available to the player
        card_count = p.count_cards()
        gen_cards = p.get_hand(Generator)
        frame_cards = p.get_hand(Frame)
        part_cards = p.get_hand(Part)

        possible_combos = []  # Check if a bot can be built
        if card_count[0] > 0 and card_count[1] > 0:
            for card1 in gen_cards:
                for card2 in frame_cards:
                    if card1.cost + card2.cost <= p.ap:
                        possible_combos.append([card1, card2])
        if len(possible_combos) > 0:
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')
            available_choices.append('Build a bot')

        possible_upgrades = []  # Check if a bot can be upgraded
        if card_count[2] > 0 and card_count[3] > 0:
            for card in part_cards:
                if card.cost <= p.ap:
                    possible_upgrades.append(card)
        if len(possible_upgrades) > 0:
            available_choices.append('Upgrade a bot')
            available_choices.append('Upgrade a bot')
            available_choices.append('Upgrade a bot')

        possible_swaps = []
        good_resources = p.get_resource_types()
        for resource in rh.pile:
            if resource not in good_resources:
                possible_swaps.append(resource)

        if p.ap >= resource_swap_cost and len(possible_swaps) > 0:
            available_choices.append('Swap a resource')
            available_choices.append('Swap a resource')
        if p.ap >= resource_refresh_cost:
            available_choices.append('Refresh all resources')
        if p.ap >= draw_cost:
            available_choices.append('Draw a card')
            available_choices.append('Draw a card')
        available_choices.append('End Turn')

        num_choice = randint(0, len(available_choices) - 1)
        choice = available_choices[num_choice]

        if choice == 'Build a bot':
            bot_built = p.ai_build(possible_combos)
            log[1].append(
                [game_num, turn_num, p.name, 'Build', bot_built.components[0].name, bot_built.components[1].name,
                 bot_built.position])
        elif choice == 'Upgrade a bot':
            [bot_upgraded, part_upgraded] = p.ai_upgrade(possible_upgrades)
            log[1].append(
                [game_num, turn_num, p.name, 'Upgrade', bot_upgraded.name, part_upgraded.name, bot_upgraded.position])
        elif choice == 'Swap a resource':
            [resource_position, old_resource, new_resource] = p.ai_swap_resource(rh)
            log[1].append([game_num, turn_num, p.name, 'Swap', old_resource, new_resource, resource_position])
        elif choice == 'Refresh all resources':
            p.refresh_resources(rh)
            log[1].append([game_num, turn_num, p.name, 'Refresh', "", "", 0])
        elif choice == 'Draw a card':
            card_drawn = p.draw()
            log[1].append([game_num, turn_num, p.name, 'Draw', card_drawn.name, "", 0])
        elif choice == 'End Turn':
            break
    p.attack(o)


if __name__ == '__main__':
    print("Lets Play!")
    start = input('[T]est or [P]lay?')
    if start == 'p' or start == 'P':
        init_game2()
    elif start == 't' or start == 'T':
        init_test()
