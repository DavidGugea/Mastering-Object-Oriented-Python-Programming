import json
from typing import Dict, Any

config = json.load(open("config.json", "r"))


def main_neste_dict(config: Dict[str, Any]) -> None:
    dealer_nm = config.get("table", {}).get("dealer", "Hit17")
    dealer_rule = {
        "Hit17": Hit17(),
        "Stand17": Stand17()
    }.get(dealer_nm, Hit17())

    split_nm = config.get("table", {}).get("split", "ReSplit")
    split_rule = {
        "ReSplit": ReSplit(),
        "NoReSplit": NoReSplit(),
        "NoReSplitAces": NoReSplitAces(),
    }.get(split_nm, ReSplit())

    decks = config.get("table", {}).get("decks", 6)
    limit = config.get("table", {}).get("limit", 100)
    payout = config.get("table", {}).get("payout", (3, 2))
    table = Table(
        decks=decks, limit=limit, dealer=dealer_rule, split=split_rule, payout=payout
    )
