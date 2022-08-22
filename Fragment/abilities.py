from player import Player

pp_gained = 2
special_pp_gained = 1


def disruption(player: Player, i: int, show=False):
    player.pp += special_pp_gained * player.bots[i].abilities.count("Disruption")
    if show:
        print(player.name, "'s bot ", player.bots[i].name, " syphoned ", special_pp_gained, " from the scrapheap.")


def reallocate(opponent: Player, i: int, show=False):
    if opponent.bots[i].abilities.count("Reallocate") > 0:
        opponent.pp += special_pp_gained
        if show:
            print(opponent.name + "'s bot " + opponent.bots[i].name + ' syphoned ' + str(
                special_pp_gained) + 'pp from opposing bot.')

