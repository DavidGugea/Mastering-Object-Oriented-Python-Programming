from Command import Command
from typing import Tuple


class Simulate_Command(Command):
    dealer_rule_map = {
        "Hit17": Hit17,
        "Stand17": Stand17
    }
    split_rule_map = {
        "ReSplit": ReSplit,
        "NoReSplit": NoReSplit,
        "NoReSplitAces": NoReSplitAces
    }
    player_rule_map = {
        "SomeStrategy": SomeStrategy,
        "AnotherStrategy": AnotherStrategy
    }
    betting_rule_map = {
        "Flat": Flat,
        "Martingale": Martingale,
        "OneThreeTwoSix": OneThreeTwoSix
    }

    def run(self) -> None:
        dealer_rule = self.dealer_rule_map[self.config["dealer_rule"]]()
        split_rule = self.split_rule_map[self.config["split_rule"]]()
        payout: Tuple[int, int]

        try:
            payout = ast.literal_eval(config.payout)
            assert len(payout) == 2
        except Exception as ex:
            raise ValueError(f"Invalid payout {config.payout}") from ex

        table = Table(
            decks=self.config["decks"],
            limit=self.config["limit"],
            dealer=dealer_rule,
            split=split_rule,
            payout=payout
        )

        player_rule = self.player_rule_map[self.config["player_rule"]]()
        betting_rule = self.betting_rule_map[self.config["betting_rule"]]()

        player = Player(
            player=player_rule,
            betting=betting_rule,
            max_rounds=self.config["rounds"],
            init_stake=self.config["stake"]
        )

        simulate = Simulate(table, player, config.samples)
        with Path(config.outputfile).open("w", newline="") as target:
            wtr = csv.writer(target)
            wtr.writerows(simulate)
