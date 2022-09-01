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
    for i in range(4):
        for card in p.hand:
            if isinstance(card, Frame):
                if card.cost - build_discount <= p.pp and p.bots[i].isblank():
                    actions_list.append(["Build", card, i])
            if isinstance(card, Generator):
                if card.cost - power_discount <= p.pp and (not p.bots[i].isblank()) and p.bots[i].num_gens < 2:
                    actions_list.append(["Power", card, i])
            if isinstance(card, Part):
                if card.cost - upgrade_discount <= p.pp and (not p.bots[i].isblank()) and p.bots[i].num_parts < 2:
                    actions_list.append(["Upgrade", card, i])
        if (not p.bots[i].isblank()) and ((p.move_cost <= p.pp) or (move_discount > p.actions.count('Move'))):
            for j in range(4):
                if p.bots[j] != p.bots[i]:
                    actions_list.append(["Move", i, j])
        for action in p.bots[i].actions:
            if (not p.bots[i].isblank()) and action != "None":
                acdf = acl.loc[acl.Name == action, "Cost"]
                if acdf.size == 0:
                    print("Tried", p.bots[i].name, "and", action, "but couldn't find it!")
                elif acdf.iloc[0] <= p.pp:
                    actions_list.append(["Action", i, action])
    if p.draw_cost - draw_discount <= p.pp and len(p.deck) > 0:
        actions_list.append(["Draw"])
    if p.resource_swap_cost - swap_discount <= p.pp:
        for i in range(4):
            actions_list.append(["Swap", i])
    if p.refresh_cost - swap_discount <= p.pp:
        actions_list.append(["Refresh"])
    return actions_list, discount_list


def rand_action(p, o, action_list, discount_list, rh, show=False, log=[]):
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
    return choice


def calc_discounts(p):
    bd = pd = ud = md = dd = sd = 0
    for i in range(4):
        bd += p.bots[i].abilities.count("Pollinate")
        pd += p.bots[i].abilities.count("Lightning")
        ud += p.bots[i].abilities.count("Fusion")
        md += p.bots[i].abilities.count("Hurricane")
        dd += p.bots[i].abilities.count("Agile")
        sd += p.bots[i].abilities.count("Frack")
    return [bd, pd, ud, md, dd, sd]


def take_action(p, o, choice, discount_list, rh, show=False, log=[]):
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
    return choice


def copy_bot(p, num, show):
    l = len(p.bots[num].components)
    for i in range(l):
        comp = p.bots[num].components[l - i - 1]
        if isinstance(comp, Frame):
            bot = Bot(comp, num)
        if isinstance(comp, Generator):
            bot.power(Generator)
        if isinstance(comp, Part):
            bot.upgrade(comp)
    bot.current_hp = p.bots[num].current_hp
    return bot


def rank_actions(p, o, rh, width, depth, show=False):
    acts = []
    for i in range(width):
        p2 = p
        p2.pp = p.pp
        o2 = o
        rh2 = rh

        # Deep copy
        for j in range(4):
            p2.bots[j] = copy_bot(p, j, show)
            o2.bots[j] = copy_bot(o, j, show)
            rh2.pile[j] = rh.pile[j]
        p2.hand = []
        for card in p.hand:
            p2.hand.append(card)

        # Run acts
        acts.append([0])
        for j in range(depth):
            al, dl = calc_actions(p2, p.action_list, p.ability_list)
            if len(al) <= 0:
                break
            act = rand_action(p2, o2, al, dl, rh2, show)
            if act[0] == "Draw":
                continue
            acts[i].append(act)

        # Calc score
        score = 0
        score += o.hp - o2.hp
        for k in range(4):
            if not p2.bots[k].isblank():
                score += p2.bots[k].resources.count(rh2.pile[k])
                score += (p2.bots[k].current_hp - p.bots[k].current_hp) / 2
        acts[i][0] = score

    print(acts)

    top_choice = [0]
    for act in acts:
        if act[0] > top_choice[0]:
            top_choice = act

    print("Choice=", top_choice)

    for choice in top_choice:
        dl = calc_discounts(p)
        if isinstance(choice, int):
            continue
        take_action(p, o, choice, dl, rh, show)

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
