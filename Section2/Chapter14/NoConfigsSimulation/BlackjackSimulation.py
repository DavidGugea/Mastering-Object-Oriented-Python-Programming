import csv


def simulate_blackjack() -> None:
    # Configuration
    dealer_rule = Hit17()
    split_rule = NoReSplitAces()
    table = Table(
        decks=6, limit=50, dealer=dealer_rule,
        split=split_rule, payout=(3, 2)
    )
    player_rule = SomeStrategy()
    betting_rule = Flat()
    player = Player(
        play=player_rule, betting=betting_rule,
        max_rounds=100, init_stake=50
    )

    # Operation
    simulator = Simulate(table, player, samples=100)
    result_path = Path.cwd() / "data" / "data.dat"
    with result_path.open("w", newline="") as results:
        wtr = csv.writer(results)
        wtr.writerows(gamestats)
