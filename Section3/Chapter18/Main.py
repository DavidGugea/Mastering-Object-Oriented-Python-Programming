import ast
import csv
import argparse
from pathlib import Path


def simulate_blackjack(config: argparse.Namespace) -> None:
    dealer_classes = {
        "Hit17": Hit17,
        "Stand17": Stand17
    }
    dealer_rule = dealer_classes[config.dealer_rule]()

    split_classes = {
        "ReSplit": ReSplit,
        "NoReSplit": NoReSplit,
        "NoReSplitAces": NoReSplitAces
    }
    split_rule = split_classes[config.split_rule]()

    try:
        payout = ast.literal_eval(config.payout)
        assert len(payout) == 2
    except Exception as ex:
        raise ValueError(f"Invalid payout {config.payout}") from ex

    table = Table(
        decks=config.decks,
        limit=config.limit,
        dealer=dealer_rule,
        split=split_rule,
        payout=payout
    )

    player_classes = {
        "SomeStrategy": SomeStrategy,
        "AnotherStrategy": AnotherStrategy
    }
    player_rule = player_classes[config.player_rule]()

    betting_classes = {
        "Flat": Flat,
        "Martingale": Martingale,
        "OneThreeTwoSix": OneThreeTwoSix
    }
    betting_rule = betting_classes[config.betting_rule]()

    player = Player(
        player=player_rule,
        betting=betting_rule,
        max_rounds=config.rounds,
        init_stake=config.init_stake
    )

    simulate = Simulate(table, player, config.samples)
    with Path(config.outputfile).open("w", newline="") as target:
        wtr = csv.writer(target)
        wtr.writerows(simulate)


main = simulate_blackjack
