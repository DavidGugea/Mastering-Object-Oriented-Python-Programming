import configparser

config = configparser.ConfigParser()
config.read('blackjack.ini')


def main_ini(config: configparser.ConfigParser) -> None:
    dealer_nm = config.get("table", "dealer", fallback="Hit17")
    dealer_rule = {
        "Hit17": Hit17(),
        "Stand17": Stand17()
    }.get(dealer_nm, Hit17())

    split_nm = config.get("table", "split", fallback="ReSplit")
    split_rule = {
        "ReSplit": ReSplit(),
        "NoReSplit": NoReSplit(),
        "NoReSplitAces": NoReSplitAces(),
    }.get(split_nm, ReSplit())

    player_nm = config.get("player", "play", fallback="SomeStrategy")
    player_rule = {
        "SomeStrategy": SomeStrategy(),
        "AnotherStrategy": AnotherStrategy(),
    }.get(player_nm, SomeStrategy())

    bet_nm = config.get("player", "betting", fallback="Flat")
    betting_rule = {
        "Flat": Flat(),
        "Martingale": Martingale(),
        "OneThreeTwoSix": OneThreeTwoSix()
    }.get(bet_nm, Flat())

    max_rounds = config.getint("player", "max_rounds", fallback=100)
    init_stake = config.getint("player", "init_stake", fallback=50)

    player = Player(
        play=player_rule,
        betting=betting_rule,
        max_rounds=max_rounds,
        init_stake=init_stake
    )

    outputfile = config.get("simulator", "outputfile", fallback="blackjack.csv")
    samples = config.getint("simulator", "samples", fallback=100)
    simulator = Simulate(table, player, samples=samples)
    with Path(outputfile).open("w", newline="") as results:
        wtr = csv.writer(results)
        wtr.writerows(simulator)


decks = config.getint("table", "decks", fallback=6)
limit = config.getint("table", "limit", fallback=100)

payout = eval(
    config.get("table", "payout", fallback="(3, 2)")
)

table = Table(
    decks=decks, limit=limit, dealer=dealer_rule,
    split=split_rule, payout=payout
)
