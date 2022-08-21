from tabulate import tabulate
from random import randint, shuffle
from card import Card, Frame, Generator, Part, Bot
from resourcesHandler import ResourceHandler
import abilities as ab

draw_cost = 1
resource_swap_cost = 1
resource_refresh_cost = 2
bot_move_cost = 1
blank_bot = Bot(Frame("Bot", "None", 0, 0, "None"))


class Player:
    def __init__(self, name: str, resource: str, deck, ai=False, strategy=[1, 1, 1, 1, 1, 1]):
        self.name = name
        self.resource = resource
        self.hp = 20
        self.deck = deck
        self.bots = [blank_bot, blank_bot, blank_bot, blank_bot]
        self.hand = []
        self.pp = 0
        self.ai = ai
        self.strategy = strategy

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

    def show_hand(self, class_name=Card):
        cards = []
        card_list = []
        for card in self.hand:
            if isinstance(card, class_name):
                card_formatted = card.listify()
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

    def show_stats(self):
        print(self.name + ' | Resource: ' + self.resource + ' | HP: ' + str(self.hp) + ' | PP: ' + str(
            self.pp) + ' | Cards: ' + str(len(self.hand)))

    # Actions
    def draw(self, show=False):
        card = self.deck.pop()
        self.hand.append(card)
        self.pp -= draw_cost
        if show:
            print(self.name + ' draws card ' + card.name)
        for i in range(4):
            ab.disruption(self, i, show)
        return card

    def build(self):

        # Select a frame
        frame_cards = self.show_hand(Frame)
        if len(frame_cards) == 0:
            print('No frames in hand!')
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
        new_bot = Bot(frame_selected, int(bot_num_selected))
        self.hand.remove(frame_selected)
        self.pp -= frame_selected.cost
        self.bots[int(bot_num_selected) - 1] = new_bot
        return 1

    def power(self):

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
        self.pp -= gen_selected.cost
        self.hand.remove(gen_selected)
        return 1

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
        self.pp -= part_selected.cost
        self.hand.remove(part_selected)

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
                self.pp -= resource_swap_cost

                # Blaze ability
                if old_resource == 'Fossil Fuel':
                    for bot in self.bots:
                        self.pp += bot.abilities.count("Blaze") * 4
                break

    def refresh_resources(self, rh: ResourceHandler, show=False):
        rh.deck = rh.pile + rh.deck
        for i in range(4):
            # Blaze ability
            if rh.pile[i] == 'Fossil Fuel':
                for bot in self.bots:
                    self.pp += bot.abilities.count("Blaze") * 4
        for i in range(4):
            rh.pile[i] = rh.deck.pop()
        self.pp -= resource_refresh_cost
        if show:
            print(self.name + ' is refreshing all resources')

    # AI methods
    def ai_build(self, possible_combos, show=False):
        choice = randint(0, len(possible_combos) - 1)
        bot_num_selected = randint(0, 3)
        frame_selected = possible_combos[choice][1]
        new_bot = Bot(frame_selected, bot_num_selected + 1)

        if show:
            print(self.name + " is building a bot using " + frame_selected.name)
        self.hand.remove(frame_selected)
        self.pp -= frame_selected.cost
        self.bots[bot_num_selected] = new_bot
        return new_bot

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
        self.pp -= part_selected.cost
        self.hand.remove(part_selected)

        return [upgrade_bots[bot_choice], part_selected]

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
            if card_selected.cost + constraint > player.pp:
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
