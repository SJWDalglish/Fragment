from tabulate import tabulate
from random import randint, shuffle
from player import Player
from card import *
from actions import attack
from resourcesHandler import ResourceHandler
import abilities as ab


# TODO: Implement abilities using event handling
class Event(object):

    def __init__(self):
        self.__eventhandlers = []

    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)


# Displays cards in a list in the console for users to select from
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


# Lists active bots in the console so that users can select one
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


def draw(p: Player, o: Player, free: bool, show=False):
    # Handle discount ability
    draw_discount = 0
    extra_cards = 0
    for i in range(4):
        draw_discount += p.bots[i].abilities.count("Agile")
        extra_cards += p.bots[i].abilities.count("Circle Back")

    # Draw cards
    for i in range(extra_cards + 1):
        card = p.deck.pop()
        p.hand.append(card)

        # Log action
        if show:
            print(p.name + ' draws card ' + card.name)

        # Post action abilities
        for j in range(4):
            ab.hp_ability(p, o, j, "Disruption", show)
            ab.pp_ability(o, j, "Sync", show)

    # Resolve payment
    p.actions.append("Draw")
    if draw_discount <= p.actions.count("Draw") and not free:
        p.pp -= p.draw_cost

    return 1


def build(p: Player, o: Player, show=False):
    # Handle discount ability
    build_discount = 0
    for i in range(4):
        build_discount += p.bots[i].abilities.count("Pollinate")

    # Select a frame
    frame_cards = p.show_hand(Frame, build_discount)
    if len(frame_cards) == 0:
        print('No frames in hand!')
        return 0
    frame_selected = select_card_list(card_list=frame_cards, player=p, select_text='Select a frame ', discount=build_discount)
    if frame_selected is None:
        return 0

    # Select a bot location
    p.show_bots()
    while True:
        bot_num_selected = select_bot_list(p, select_text='Select a build location ')
        if bot_num_selected is None:
            return 0
        if not p.bots[int(bot_num_selected) - 1].isblank():
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
    p.hand.remove(frame_selected)
    p.pp -= max(0, frame_selected.cost - build_discount)
    p.bots[int(bot_num_selected) - 1] = new_bot

    # Post action abilities
    for i in range(4):
        ab.hp_ability(p, o, i, "Leech", show)
        ab.pp_ability(o, i, "Hunger", show)

    # Log action
    if show:
        print(p.name + ' built ' + new_bot.name)
    p.actions.append("Build")
    return 1


def power(p: Player, o: Player, show=False):
    # Handle discount ability
    power_discount = 0
    for i in range(4):
        power_discount += p.bots[i].abilities.count("Lightning")

    # Select a bot location
    p.show_bots()
    while True:
        bot_selected = select_bot_list(p, 'Select a bot to upgrade ')
        if bot_selected is None:
            return 0
        if p.bots[int(bot_selected) - 1].isblank():
            print('No bot selected.')
            continue
        break

    # Select a generator
    gen_cards = p.show_hand(Generator, power_discount)
    if len(gen_cards) == 0:
        print('No generators in hand!')
        return 0
    gen_selected = select_card_list(gen_cards, p, 'Select a generator ', power_discount)
    if gen_selected is None:
        return 0

    # Clean up
    p.bots[int(bot_selected) - 1].power(gen_selected)
    p.pp -= max(0, gen_selected.cost - power_discount)
    p.hand.remove(gen_selected)

    # Post action abilities
    for i in range(4):
        ab.hp_ability(p, o, i, "Recharge", show)
        ab.pp_ability(o, i, "Charge", show)

    # Log action
    if show:
        print(p.name + ' powered ' + p.bots[int(bot_selected) - 1].name)
    p.actions.append("Power")
    return 1


def upgrade(p: Player, o: Player, show=False):
    # Handle discount ability
    upgrade_discount = 0
    for i in range(4):
        upgrade_discount += p.bots[i].abilities.count("Fusion")

    # Select a bot location
    p.show_bots()
    while True:
        bot_selected = select_bot_list(p, 'Select a bot to upgrade ')
        if bot_selected is None:
            return 0
        if p.bots[int(bot_selected) - 1].isblank():
            print('No bot selected.')
            continue
        break

    # Select a part
    part_cards = p.show_hand(Part)
    if len(part_cards) == 0:
        print('No generators in hand!')
        return 0
    part_selected = select_card_list(part_cards, p, 'Select a part ')
    if part_selected is None:
        return 0

    # Clean up
    p.bots[int(bot_selected) - 1].upgrade(part_selected)
    p.pp -= min(0, part_selected.cost - upgrade_discount)
    p.hand.remove(part_selected)

    # Post action abilities
    for i in range(4):
        ab.hp_ability(p, o, i, "Mutate", show)
        ab.pp_ability(o, i, "Research", show)

    # Log action
    if show:
        print(p.name + ' upgraded ' + p.bots[int(bot_selected) - 1].name)
    p.actions.append("Upgrade")
    return 1


def move(player: Player, opp: Player, show=False):
    # Handle discount ability
    move_discount = 0
    for i in range(4):
        move_discount += player.bots[i].abilities.count("Hurricane")

    # Select a bot to move
    player.show_bots()
    while True:
        num_one_selected = select_bot_list(player, 'Select a bot to move ')
        if num_one_selected is None:
            return 0
        if player.bots[int(num_one_selected) - 1].isblank():
            print('No bot selected.')
            continue
        break
    b1 = int(num_one_selected)

    # Select a bot location
    player.show_bots()
    while True:
        num_two_selected = select_bot_list(player, 'Select a location to move to ')
        if num_two_selected is None:
            return 0
        if player.bots[int(num_two_selected) - 1].isblank():
            print('No bot selected.')
            continue
        break
    b2 = int(num_two_selected)

    # Swap bots
    tmp_bot = player.bots[b1]
    player.bots[b1] = player.bots[b2]
    player.bots[b2] = tmp_bot

    # Resolve power cost
    if move_discount <= player.actions.count("Move"):
        player.pp -= player.move_cost

    # Post action abilities
    for i in range(4):
        ab.hp_ability(player, opp, i, "Rain Recollection", show)
        ab.pp_ability(opp, i, "Backdraft", show)

    # Log action
    if show:
        print(player.name + ' moved ' + player.bots[b1 - 1].name)
    player.actions.append("Move")
    return 1


def swap_resource(player: Player, opp: Player, rh: ResourceHandler, show=False):
    # Handle discount ability
    swap_discount = 0
    for i in range(4):
        swap_discount += player.bots[i].abilities.count("Frack")

    # Select a resource
    rh.list_pile()
    while True:
        num_choice = input('Select a resource to swap or press [x] to cancel.')
        if num_choice == 'x':
            return 0
        if num_choice in [str(x) for x in range(4)]:
            o, n = rh.swap_resource(int(num_choice))
            if swap_discount <= player.actions.count("Swap"):
                player.pp -= player.resource_swap_cost

            # Blaze ability
            if o == 'Fossil Fuel':
                for bot in player.bots:
                    player.pp += bot.abilities.count("Blaze") * 4
            break

    # Post action abilities
    for i in range(4):
        ab.hp_ability(player, opp, i, "Burn", show)
        ab.pp_ability(opp, i, "Spoils", show)

    # Log action
    if show:
        print(player.name + ' swapped ' + o + ' for ' + n)
    player.actions.append("Swap")
    return 1


def refresh_resources(player: Player, opp: Player, rh: ResourceHandler, show=False):
    # Handle discount ability
    swap_discount = 0
    for i in range(4):
        swap_discount += player.bots[i].abilities.count("Frack")

    rh.deck = rh.pile + rh.deck

    # Blaze ability
    for i in range(4):
        if rh.pile[i] == 'Fossil Fuel':
            for bot in player.bots:
                player.pp += bot.abilities.count("Blaze") * 4

    # Draw new resources
    for i in range(4):
        rh.pile[i] = rh.deck.pop()
    if swap_discount <= player.actions.count("Swap"):
        player.pp -= 2 * player.resource_swap_cost
    else:
        player.pp -= player.resource_swap_cost

    # Log action
    if show:
        print(player.name + ' refreshed all resources ')
    player.actions.append("Refresh")
    return 1


def select_attack_list(p: Player, bot_num: int, select_text: str, show=False):
    p.bots[bot_num].display_actions()
    while True:
        num_selected = input(select_text + 'or press [x] to cancel.')
        if num_selected == 'x':
            return None
        elif not num_selected.isdecimal():
            print('Not a valid input.')
            continue
        elif int(num_selected) in [x + 1 for x in list(range(len(p.bots[bot_num].actions)))]:
            return num_selected
        print('Not a valid input.')
        continue
    return None


def take_action(p: Player, o: Player, rh: ResourceHandler, show=False):
    n = select_bot_list(p, "Select bot to attack with ")
    if n is None:
        return 0

    m = select_attack_list(p, int(n), "Select an action to take ", show)
    if n is None:
        return 0

    attack(p, o, int(n), p.bots[n].actions[int(m)-1], show)
    return 1


# TODO: Refactor and update
def generate_pp(p: Player, o: Player, rh: ResourceHandler, show=False):
    pp_gained = p.default_pp_gained
    special_pp_gained = p.special_pp_gained

    for i in range(4):
        bot = p.bots[i]
        if bot.isblank():
            continue

        # Gain PP from adjacent resource
        p.gen_pp(bot_num=i, pp_gain=pp_gained, source=bot.resources.count(rh.pile[i]), show=show)
        o.gen_pp(i, o.bots[i].abilities.count("Acquire") * special_pp_gained, "Acquire", show)

        # PP from Radiate
        if bot.abilities.count("Radiate") > 0:
            p.gen_pp(i, bot.abilities.count("Radiate") * special_pp_gained, "Radiate", show)
            o.gen_pp(i, o.bots[i].abilities.count("Acquire") * special_pp_gained, "Acquire", show)

        # PP from Storm Drain
        if bot.abilities.count("Storm Drain") > 0:
            pp_gain = 0
            for j in range(4):
                if (j != i) and (rh.pile[j] == 'Weather Event'):
                    pp_gain += special_pp_gained
            p.gen_pp(i, bot.abilities.count("Storm Drain") * pp_gain, "Storm Drain", show)
            o.gen_pp(i, o.bots[i].abilities.count("Acquire") * special_pp_gained, "Acquire", show)

        # PP from Pack
        if bot.abilities.count("Pack") > 0:
            pp_gain = 0
            for j in range(4):
                if (j != i) and (not p.bots[j].isblank()):
                    pp_gain += special_pp_gained
            p.gen_pp(i, bot.abilities.count("Pack") * pp_gain, "Pack", show)
            o.gen_pp(i, o.bots[i].abilities.count("Acquire") * special_pp_gained, "Acquire", show)
