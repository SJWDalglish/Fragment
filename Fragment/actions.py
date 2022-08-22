from tabulate import tabulate
from random import randint, shuffle
from player import Player
from card import *
from resourcesHandler import ResourceHandler
import abilities as ab


def select_card_list(card_list: [Card], player: Player, select_text: str, discount=0):
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
            if card_selected.cost - discount > player.pp:
                print("Not enough PP!")
                continue
            return card_selected
        print('Not a valid input.')
        continue
    return None


def select_bot_list(player: Player, select_text: str):
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


def draw(player: Player, show=False):
    # Handle discount ability
    draw_discount = 0
    for i in range(4):
        draw_discount += player.bots[i].abilities.count("Agile")

    card = player.deck.pop()
    player.hand.append(card)
    if draw_discount <= player.actions.count("Draw"):
        player.pp -= player.draw_cost

    # Log action
    if show:
        print(player.name + ' draws card ' + card.name)
    player.actions.append("Draw")

    for i in range(4):
        ab.disruption(player, i, show)

    return card


def build(player: Player, show=False):
    # Handle discount ability
    build_discount = 0
    # if player.actions.count("Build") == 0:
    for i in range(4):
        build_discount += player.bots[i].abilities.count("Pollinate")

    # Select a frame
    frame_cards = player.show_hand(Frame, build_discount)
    if len(frame_cards) == 0:
        print('No frames in hand!')
        return 0
    frame_selected = select_card_list(frame_cards, player, 'Select a frame ')
    if frame_selected is None:
        return 0

    # Select a bot location
    player.show_bots()
    while True:
        bot_num_selected = select_bot_list(player, 'Select a build location ')
        if bot_num_selected is None:
            return 0
        if not player.bots[int(bot_num_selected) - 1].isblank():
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

    # Clean up hand, minus pp, add bot
    new_bot = Bot(frame_selected, int(bot_num_selected))
    player.hand.remove(frame_selected)
    player.pp -= min(0, frame_selected.cost - build_discount)
    player.bots[int(bot_num_selected) - 1] = new_bot

    # Log action
    if show:
        print(player.name + ' built ' + new_bot.name)
    player.actions.append("Build")
    return 1


def power(player: Player, show=False):
    # Handle discount ability
    power_discount = 0
    # if player.actions.count("Power") == 0:
    for i in range(4):
        power_discount += player.bots[i].abilities.count("Lightning")

    # Select a bot location
    player.show_bots()
    while True:
        bot_selected = select_bot_list(player, 'Select a bot to upgrade ')
        if bot_selected is None:
            return 0
        if player.bots[int(bot_selected) - 1].isblank():
            print('No bot selected.')
            continue
        break

    # Select a generator
    gen_cards = player.show_hand(Generator, power_discount)
    if len(gen_cards) == 0:
        print('No generators in hand!')
        return 0
    gen_selected = select_card_list(gen_cards, player, 'Select a generator ')
    if gen_selected is None:
        return 0

    # Clean up
    player.bots[int(bot_selected) - 1].power(gen_selected)
    player.pp -= min(0, gen_selected.cost - power_discount)
    player.hand.remove(gen_selected)
    player.deck.append(gen_selected)

    # Log action
    if show:
        print(player.name + ' powered ' + player.bots[int(bot_selected) - 1].name)
    player.actions.append("Power")
    return 1


def upgrade(player: Player, show=False):
    # Handle discount ability
    upgrade_discount = 0
    # if player.actions.count("Power") == 0:
    for i in range(4):
        upgrade_discount += player.bots[i].abilities.count("Fusion")

    # Select a bot location
    player.show_bots()
    while True:
        bot_selected = select_bot_list(player, 'Select a bot to upgrade ')
        if bot_selected is None:
            return 0
        if player.bots[int(bot_selected) - 1].isblank():
            print('No bot selected.')
            continue
        break

    # Select a part
    part_cards = player.show_hand(Part)
    if len(part_cards) == 0:
        print('No generators in hand!')
        return 0
    part_selected = select_card_list(part_cards, player, 'Select a part ')
    if part_selected is None:
        return 0

    # Clean up
    player.bots[int(bot_selected) - 1].upgrade(part_selected)
    player.pp -= part_selected.cost
    player.hand.remove(part_selected)

    # Log action
    if show:
        print(player.name + ' upgraded ' + player.bots[int(bot_selected) - 1].name)
    player.actions.append("Upgrade")
    return 1


def swap_resource(player: Player, rh: ResourceHandler, show=False):
    rh.list_pile()
    while True:
        num_choice = input('Select a resource to swap or press [x] to cancel.')
        if num_choice == 'x':
            return 0
        if num_choice in [str(x) for x in range(4)]:
            o, n = rh.swap_resource(int(num_choice))
            player.pp -= resource_swap_cost

            # Blaze ability
            if o == 'Fossil Fuel':
                for bot in player.bots:
                    player.pp += bot.abilities.count("Blaze") * 4
            break

    # Log action
    if show:
        print(player.name + ' swapped ' + o + ' for ' + n)
    player.actions.append("Swap")
    return 1


def refresh_resources(player, rh: ResourceHandler, show=False):
    rh.deck = rh.pile + rh.deck

    # Blaze ability
    for i in range(4):
        if rh.pile[i] == 'Fossil Fuel':
            for bot in player.bots:
                player.pp += bot.abilities.count("Blaze") * 4

    # Draw new resources
    for i in range(4):
        rh.pile[i] = rh.deck.pop()
    player.pp -= resource_refresh_cost
    if show:
        print(player.name + ' is refreshing all resources')

    # Log action
    if show:
        print(player.name + ' refreshed all resources ')
    player.actions.append("Refresh")
    return 1


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
