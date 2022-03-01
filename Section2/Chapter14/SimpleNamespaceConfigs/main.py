import types

config2c = types.SimpleNamespace(
    dealer_rule=Hit17(),
    split_rule=NoReSplitAces(),
    player_rule=SomeStrategy(),
    betting_rule=Flat(),
    outputfile=Path.cwd() / "data" / "data.dat",
    samples=100,
)
config2c.table = Table(
    decks=6,
    limit=50,
    dealer=config2c.dealer_rule,
    split=config2c.split_rule,
    playout=(3, 2),
)
config2c.player = Player(
    play=config2c.player_rule,
    betting=config2c.betting_rule,
    max_rounds=100,
    init_stake=50
)
