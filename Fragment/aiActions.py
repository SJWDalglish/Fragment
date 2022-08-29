from tabulate import tabulate
import random
from random import randint, shuffle, choice

import actions
import playerActions
from player import Player
from card import Card, Frame, Generator, Part, Bot
from resourcesHandler import ResourceHandler
import abilities as ab

# Action costs
draw_cost = 1
resource_swap_cost = 1
resource_refresh_cost = 2
bot_move_cost = 1


def calc_actions(p: Player, acl, abl):
    # Handle discount ability
    build_discount = 0
    power_discount = 0
    upgrade_discount = 0
    move_discount = 0
    draw_discount = 0
    swap_discount = 0
    for i in range(4):
        build_discount += p.bots[i].abilities.count("Pollinate")
        power_discount += p.bots[i].abilities.count("Lightning")
        upgrade_discount += p.bots[i].abilities.count("Fusion")
        move_discount += p.bots[i].abilities.count("Hurricane")
        draw_discount += p.bots[i].abilities.count("Agile")
        swap_discount += p.bots[i].abilities.count("Frack")
    discount_list = [build_discount, power_discount, upgrade_discount, move_discount, draw_discount, swap_discount]

    actions_list = []
    movable = False
    for card in p.hand:
        for bot in p.bots:
            if isinstance(card, Frame):
                if card.cost - build_discount <= p.pp and bot.isblank():
                    actions_list.append(["Build", card, bot.position])
            if isinstance(card, Generator):
                if card.cost - power_discount <= p.pp and not bot.isblank() and bot.num_gens < 2:
                    actions_list.append(["Power", card, bot.position])
            if isinstance(card, Part):
                if card.cost - upgrade_discount <= p.pp and not bot.isblank() and bot.num_parts < 2:
                    actions_list.append(["Upgrade", card, bot.position])
    for bot in p.bots:
        if not bot.isblank() and (p.move_cost - move_discount <= p.pp):
            for b2 in p.bots:
                if b2 != bot:
                    actions_list.append(["Move", bot.position, b2.position])
        for action in bot.actions:
            if not bot.isblank() and action != "None":
                acdf = acl.loc[acl.Name == action, "Cost"]
                if acdf.size == 0:
                    print("Tried", bot.name, "and", action, "but couldn't find it!")
                elif acdf.iloc[0] <= p.pp:
                    actions_list.append(["Action", bot.position, action])
    if p.draw_cost - draw_discount <= p.pp and len(p.deck) > 0:
        actions_list.append(["Draw"])
    if p.resource_swap_cost - swap_discount <= p.pp:
        for i in range(4):
            actions_list.append(["Swap", i])
    if p.refresh_cost - swap_discount <= p.pp:
        actions_list.append(["Refresh"])
    return actions_list, discount_list


def rand_action(p, o, action_list, discount_list, rh, show=False):
    choice = random.choice(action_list)
    match choice[0]:
        case "Build":
            playerActions.build_bot(p, o, choice[1], choice[2], discount_list[0], show)
        case "Power":
            playerActions.power_bot(p, o, choice[1], choice[2], discount_list[1], show)
        case "Upgrade":
            playerActions.upgrade_bot(p, o, choice[1], choice[2], discount_list[2], show)
        case "Move":
            playerActions.move_bot(p, o, choice[1], choice[2], discount_list[3], show)
        case "Action":
            actions.attack(p, o, choice[1], choice[2], show)
        case "Draw":
            playerActions.draw(p, o, False, show)
        case "Swap":
            playerActions.swap_chosen_resource(p, o, choice[1], discount_list[5], rh, show)
        case "Refresh":
            playerActions.refresh_resources(p, o, rh, show)
    return 1


# AI methods
def ai_build(player: Player, possible_combos, show=False):
    choice = randint(0, len(possible_combos) - 1)
    bot_num_selected = randint(0, 3)
    frame_selected = possible_combos[choice][1]
    new_bot = Bot(frame_selected, bot_num_selected + 1)

    if show:
        print(player.name + " is building a bot using " + frame_selected.name)
    player.hand.remove(frame_selected)
    player.pp -= frame_selected.cost
    player.bots[bot_num_selected] = new_bot
    return new_bot


def ai_upgrade(player: Player, possible_upgrades, show=False):
    upgrade_bots = []
    for bot in player.bots:
        if not bot.isblank():
            upgrade_bots.append(bot)
    bot_choice = randint(0, len(upgrade_bots) - 1)
    part_choice = randint(0, len(possible_upgrades) - 1)
    part_selected = possible_upgrades[part_choice]

    if show:
        print(player.name + " is upgrading " + upgrade_bots[bot_choice].name + ' with ' + part_selected.name)
    upgrade_bots[bot_choice].upgrade(part_selected)
    player.pp -= part_selected.cost
    player.hand.remove(part_selected)

    return [upgrade_bots[bot_choice], part_selected]

def ai_swap_resource(player: Player, rh, show=False, possible_swaps=[]):
    if possible_swaps == []:
        good_resources = player.get_resource_types()
        for i in range(4):
            if rh.pile[i] not in good_resources:
                possible_swaps.append(i)
    num_choice = randint(0, len(possible_swaps) - 1)
    old_resource = rh.pile[possible_swaps[num_choice]]
    new_resource = rh.deck.pop()
    rh.pile[possible_swaps[num_choice]] = new_resource
    rh.deck.insert(0, old_resource)
    player.ap -= resource_swap_cost
    if show:
        print(player.name + ' is swapping resource ' + old_resource + ' for ' + new_resource)
    return [num_choice, old_resource, new_resource]