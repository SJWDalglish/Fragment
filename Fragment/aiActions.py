from tabulate import tabulate
from random import randint, shuffle
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

    actions_list = []
    movable = False
    for card in p.hand:
        if isinstance(card, Frame):
            if card.cost - build_discount <= p.pp:
                actions_list.append(["Build", card])
        if isinstance(card, Generator):
            if card.cost - power_discount <= p.pp:
                actions_list.append(["Power", card])
        if isinstance(card, Part):
            if card.cost - upgrade_discount <= p.pp:
                actions_list.append(["Upgrade", card])
    for bot in p.bots:
        if not bot.isblank() and (p.move_cost - move_discount <= p.pp):
            actions_list.append(["Move", bot])
        for action in bot.actions:
            if acl.loc[acl.Name == action, "Cost"].iloc[0] <= p.pp:
                actions_list.append(["Action", bot, action])
    if p.draw_cost - draw_discount <= p.pp:
        actions_list.append(["Draw"])
    if p.resource_swap_cost - swap_discount <= p.pp:
        actions_list.append(["Swap"])
    if p.refresh_cost - swap_discount <= p.pp:
        actions_list.append(["Refresh"])
    return actions_list


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