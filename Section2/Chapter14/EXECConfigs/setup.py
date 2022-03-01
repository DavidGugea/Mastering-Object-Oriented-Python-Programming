# Setup

# Table
dealer_rule = Hit17()
split_rule = NoReSplitAces()
table = Table(decks=6, limit=50, dealer=dealer_rule, split=split_rule, payout=(3, 2))

# Player
player_rule = SomeStrategy()
betting_rule = Flat()
player = PLayer(play=player_rule, betting=betting_rule, max_rounds=100, init_stake=50)

# Simulation
outputfile = Path.cwd() / "data" / "data.dat"
samples = 100
