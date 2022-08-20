import pandas as pd
import numpy as np
import abilities as ab

from card import Card, Frame, Generator, Part, Bot
from player import Player
from random import randint, shuffle
from tabulate import tabulate

import datetime

types = ["Acquire", "Augment", "Consume", "Convert", "Cultivate", "Preserve"]
resource_types = ["Biomass", "Power Cell", "Fossil Fuel", "Radioactive Material", "Weather Event"]
pp_per_turn = 3
num_resources = 6
hand_start_size = 6
hand_draw_size = 1
p1_start_pp = 5
p2_start_pp = 6
num_generators = 3
num_frames = 3
num_parts = 1
draw_cost = 1
resource_swap_cost = 1
resource_refresh_cost = 2
bot_move_cost = 1
pp_gained = 2
special_pp_gained = 1


class Ability:
    def __init__(self, name: str, ability_type: str, cost: int, desc: str, dmg: int):
        self.name = name
        self.ability_type = ability_type
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


blank_bot = Bot(Frame("Bot", "None", 0, 0, "None"))


def generate_pp(player, opponent, resource_handler, show=False):
    for i in range(4):
        bot = player.bots[i]
        if bot.isblank():
            continue

        # Gain PP from adjacent resource
        if bot.resources.count(resource_handler.pile[i]) > 0:
            player.pp += pp_gained
            if show:
                print(player.name + "'s bot " + player.bots[i].name + ' regained ' + str(
                    pp_gained) + 'pp using adjacent resource.')
            if opponent.bots[i].abilities.count("Reallocate") > 0:
                opponent.pp += special_pp_gained
                if show:
                    print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                        special_pp_gained) + 'pp from opposing bot.')

        # PP from Radiate
        if bot.abilities.count('Radiate') > 0:
            self.pp += special_pp_gained * (len(bot.components) - 2)
            if show:
                print(self.name + "'s bot " + self.bots[i].name + ' regained ' + str(
                    special_pp_gained * (len(bot.components) - 2)) + 'pp using repurposed hardware.')
            if opponent.bots[i].abilities.count("Reallocate") > 0:
                opponent.pp += special_pp_gained
                if show:
                    print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                        special_pp_gained) + 'pp from opposing bot.')

        # PP from Storm Drain
        if bot.abilities.count('Storm Drain') > 0:
            for j in range(4):
                if (j != i) and (resource_handler.pile[j] == 'Weather Event'):
                    self.pp += special_pp_gained
                    if show:
                        print(self.name + "'s bot " + self.bots[i].name + ' regained ' + str(
                            special_pp_gained) + 'pp due to inclement weather.')
                    if opponent.bots[i].abilities.count("Reallocate") > 0:
                        opponent.pp += special_pp_gained
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
