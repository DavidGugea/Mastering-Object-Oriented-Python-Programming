from simulator import *


def simulate_SomeStrategy_Flat() -> None:
    dealer_rule = Hit17()
    split_rule = NoReSplitAces()
    table = Table(
        decks=6, limit=50, dealer=dealer_rule, split=split_rule, payout=(3, 2)
    )

    player_rule = SomeStrategy()
    betting_rule = Flat()
    player = Player(
        play=player_rule, betting=betting_rule, max_rounds=100, init_stake=50
    )
    simulate(table, player, Path.cwd()/"data"/"data.dat", 100)


if __name__ == '__main__':
    simulate_SomeStrategy_Flat()