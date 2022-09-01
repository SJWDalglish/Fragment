import pandas as pd
import numpy as np
import abilities as ab
import os

import aiActions
from card import *
from player import Player
from playerActions import *
from aiActions import *
from random import randint, shuffle
from resourcesHandler import ResourceHandler
from tabulate import tabulate

import datetime

# TODO: Refactor code and import modules

types = ["Acquire", "Augment", "Consume", "Convert", "Cultivate", "Preserve", "Tinker"]
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


def choose_deck(deck_user: str):
    while True:
        player_type_num = input("Choose a deck for " + deck_user + "!"
                                "\n[1] Acquire"
                                "\n[2] Augment"
                                "\n[3] Consume"
                                "\n[4] Convert"
                                "\n[5] Cultivate"
                                "\n[6] Preserve"
                                "\n[7] Tinker"
                                "\n[8] Show Details"
                                "\n[9] Exit")
        if not (["1", "2", "3", "4", "5", "6", "7", "8", "9"].count(player_type_num) > 0):
            print("Not an available option!")
            continue
        if player_type_num in ["1", "2", "3", "4", "5", "6", "7"]:
            player_type = types[int(player_type_num) - 1]
            break
        if player_type_num == "8":
            print("Acquire: Steal opponents' PP."
                  "\nAugment: Gain PP from attached parts."
                  "\nConsume: Burn resources for a quick PP gain."
                  "\nConvert: Gain PP from all weather events."
                  "\nCultivate: Gain PP from all friendly bots."
                  "\nPreserve: Gain extra PP from Power Cells."
                  "\nTinker: Gain a small amount of PP from all resources.")
        if player_type_num == "9":
            return None
    return player_type


def init_decks():
    player_type = types[randint(0, 5)]
    opponent_type = types[randint(0, 5)]

    while True:
        player_game_style = input(
            "How do you want to play?\n[1] Against an AI\n[2] Against myself\n[3] Watch the AI play")
        if not (["1", "2", "3"].count(player_game_style) > 0):
            print("Not an available option!")
            continue
        break

    if player_game_style == "1":
        player_type = choose_deck("you")
        if player_type is None:
            return None, None, None, None

    if player_game_style == "2":
        player_type = choose_deck("you")
        if player_type is None:
            return None, None, None
        opponent_type = choose_deck("your opponent")
        if opponent_type is None:
            return None, None, None, None

    player_deck = []
    opponent_deck = []

    [generators, frames, parts, acl, abl] = prep_cards()

    for card in generators:
        if card.deck == player_type:
            player_deck.extend(num_generators * list([card]))
        if card.deck == opponent_type:
            opponent_deck.extend(num_generators * list([card]))
    for card in frames:
        if card.deck == player_type:
            player_deck.extend(num_frames * list([card]))
        if card.deck == opponent_type:
            opponent_deck.extend(num_frames * list([card]))
    for card in parts:
        player_deck.extend(num_parts * list([card]))
        opponent_deck.extend(num_parts * list([card]))

    shuffle(player_deck)
    shuffle(opponent_deck)
    player_ai = player_game_style == "3"
    opponent_ai = (player_game_style == "1" or player_game_style == "3")

    player = Player("Player 1", player_type, player_deck, acl, abl, player_ai)
    opponent = Player("Player 2", opponent_type, opponent_deck, acl, abl, opponent_ai)

    resource_handler = ResourceHandler()

    while True:
        show_num = input(
            "How do you want to play?\n[1] Show descriptions\n[2] Hide descriptions")
        if not (["1", "2"].count(show_num) > 0):
            print("Not an available option!")
            continue
        break
    if int(show_num) == 1:
        show = True
    else:
        show = False

    return player, opponent, resource_handler, show


def init_game():
    player1, player2, resource_handler, show = init_decks()
    if player1 is None:
        return None
    for i in range(hand_start_size):
        player1.draw()
        player2.draw()
    turn = randint(0, 1)
    if turn == 0:
        player1.pp = p1_start_pp
        player2.pp = p2_start_pp
    else:
        player1.pp = p2_start_pp
        player2.pp = p1_start_pp
    winner = game_manager(turn, player1, player2, resource_handler, show)
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


def take_turn_ai(p, o, rh, show=False, log=[]):
    for i in range(10):
        poss_actions, discount_list = aiActions.calc_actions(p, p.action_list, p.ability_list)
        if len(poss_actions) > 0:
            aiActions.rand_action(p, o, poss_actions, discount_list, rh, show)
    return 1


def take_turn(player, opponent, resource_handler, show=False, log=[]):
    generate_pp(player, opponent, resource_handler, show)  # Generate PP for bots according to associated resources
    player.pp += pp_per_turn  # Update PP
    for i in range(hand_draw_size):
        draw(player, opponent, True, show)  # Draw a card

    output = 1

    if player.ai:
        output = take_turn_ai(player, opponent, resource_handler, show)
    else:
        output = take_turn_player(player, opponent, resource_handler, show)

    return output


def take_turn_player(player, opponent, resource_handler, show=False):
    while True:  # Iterate through choices available during turn
        display_field(player, opponent, resource_handler)
        available_choices = []  # Used to track choices available to the player

        # See if an action is possible
        for bot in player.bots:
            if not bot.isblank():
                available_choices.append('Take action')
                break

        card_count = player.count_cards()
        if card_count[0] > 0:
            available_choices.append('Build a bot')
        if card_count[1] > 0 and card_count[3] > 0:
            available_choices.append('Power a bot')
        if card_count[2] > 0 and card_count[3] > 0:
            available_choices.append('Upgrade a bot')
        if player.pp >= bot_move_cost:
            available_choices.append('Move a bot')
        if player.pp >= resource_swap_cost:
            available_choices.append('Swap a resource')
        if player.pp >= resource_refresh_cost:
            available_choices.append('Refresh all resources')
        if player.pp >= draw_cost:
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
        match choice:
            case 'Take action':
                take_action(player, opponent, resource_handler, show)
            case 'Build a bot':
                build(player, opponent, show)
            case 'Power a bot':
                power(player, opponent, show)
            case 'Upgrade a bot':
                upgrade(player, opponent, show)
            case 'Move a bot':
                move(player, opponent, show)
            case 'Swap a resource':
                swap_resource(player, opponent, resource_handler, show)
            case 'Refresh all resources':
                refresh_resources(player, opponent, resource_handler, show)
            case 'Draw a card':
                draw(player, opponent, show)
            case 'End Turn':
                break
            case 'Exit Game':
                return 0
    return 1


# TODO: get csv files and integrate them
def prep_cards():
    # abilities = pd.read_csv('Fragment 1.0 CSV Files/Abilities.csv')
    frames = pd.read_csv('CSV/Frames.csv')
    generators = pd.read_csv('CSV/Generators.csv')
    parts = pd.read_csv('CSV/Parts.csv')
    action_list = pd.read_csv('CSV/Actions.csv')
    ability_list = pd.read_csv('CSV/Abilities.csv')

    frame_list = []
    for index, row in frames.iterrows():
        frame_list.append(Frame(row['Name'], row['Deck'], row['Cost'], row['HP'], row['Desc'], row['Action 1'], row['Action 2']))

    generator_list = []
    for index, row in generators.iterrows():
        generator_list.append(Generator(row['Name'], row['Deck'], row['Cost'], row['HP'], row['Desc'], row['Ability 1'], row['Ability 2']))

    part_list = []
    for index, row in parts.iterrows():
        part_list.append(Part(row['Name'], row['Cost'], row['HP'], row['Desc'], row['Action']))

    return [frame_list, generator_list, part_list, action_list, ability_list]


def display_field(player: Player, opponent: Player, resource_handler: ResourceHandler):
    print('\n' + ('+' * 50) + '\n')
    opponent.show_stats()
    field = opponent.listify_bots()
    field.extend([["*--------------*"] * 4, resource_handler.pile, ["*--------------*"] * 4])
    field.extend(player.listify_bots())
    print(tabulate(field))
    # opponent.show_bots()
    # resource_handler.show_pile()
    # player.show_bots()
    player.show_stats()
    player.show_hand()
    print('\n' + ('+' * 50) + '\n')


def init_test():
    status_log = ['Game', 'Turn', 'Player', 'Object', 'Position', 'Stat', 'Value']
    activity_log = ['Game', 'Turn', 'Player', 'Action', 'Component1', 'Component2']
    win_log = ['Game', 'Turns', 'Player1_Type', 'Player2_Type', 'Winner']
    log = [[], [], []]
    while True:
        num = input('How many iterations?')
        if num.isdecimal():
            for i in range(int(num)):
                print('[', end='')
                result = run_test_game(i, log)
                log[2].append([str(i)] + result)
                print(']')
            now = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
            # pd.DataFrame(log[0],columns=status_log).to_csv('CSV/'+now+'_test_status_log.csv', index=False)
            pd.DataFrame(log[1], columns=activity_log).to_csv('CSV/' + now + '_test_activity_log.csv', index=False)
            pd.DataFrame(log[2], columns=win_log).to_csv('CSV/' + now + '_test_win_log.csv', index=False)
            break
        else:
            print('Please enter an integer.')


def run_test_game(game_num: int, log):
    [generators, frames, parts, acl, abl] = prep_cards()
    player1_type = types[randint(0, 5)]
    player2_type = types[randint(0, 5)]
    player_deck = []
    opponent_deck = []
    for card in generators:
        if card.deck == player1_type:
            player_deck.extend(num_generators * list([card]))
        if card.deck == player2_type:
            opponent_deck.extend(num_generators * list([card]))
    for card in frames:
        if card.deck == player1_type:
            player_deck.extend(num_frames * list([card]))
        if card.deck == player2_type:
            opponent_deck.extend(num_frames * list([card]))
    for card in parts:
        player_deck.extend(num_parts * list([card]))
        opponent_deck.extend(num_parts * list([card]))

    shuffle(player_deck)
    shuffle(opponent_deck)
    p1 = Player("Player 1", player1_type, player_deck, acl, abl, True)
    p2 = Player("Player 2", player2_type, opponent_deck, acl, abl, True)
    rh = ResourceHandler()

    turn = 0
    p2.pp += 1
    turn_num = 0
    while p1.hp > 0 and p2.hp > 0:
        turn_num += 1
        print('-', end='')
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
        if turn_num >= 100:
            break
    if p1.hp <= 0:
        return [turn_num, p1.resource, p2.resource, p2.name]
    elif p2.hp <= 0:
        return [turn_num, p1.resource, p2.resource, p1.name]
    else:
        return [turn_num, p1.resource, p2.resource, "Draw"]


def test_turn(p: Player, o: Player, rh: ResourceHandler, game_num: int, turn_num: int, log):
    generate_pp(p, o, rh)  # Generate PP for bots according to associated resources
    p.pp += pp_per_turn  # Update PP
    for i in range(hand_draw_size):
        draw(p, o, True)  # Draw a card

    for i in range(10):
        available_actions, discount_list = calc_actions(p, p.action_list, p.ability_list)
        if len(available_actions)>0:
            c = rand_action(p, o, available_actions, discount_list, rh)
            if len(c) < 3:
                c.append("None")
                if len(c) < 3:
                    c.append("None")
            if isinstance(c[1], Card):
                c[1] = c[1].name
            log[1].append([game_num, turn_num, p.name, c[0], c[1], c[2]])
        else:
            break
    return 1


if __name__ == '__main__':
    print("Lets Play!")
    start = input('[T]est or [P]lay?')
    if start == 'p' or start == 'P':
        init_game()
    elif start == 't' or start == 'T':
        init_test()
