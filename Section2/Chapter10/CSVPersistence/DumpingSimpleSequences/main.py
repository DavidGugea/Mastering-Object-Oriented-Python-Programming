from typing import NamedTuple, Iterator, Type
import random
import csv
from pathlib import Path


class GameStat(NamedTuple):
    player: str
    bet: str
    rounds: int
    final: float


def gamestat_iter(
        player: Type[Player_Strategy],
        betting: Type[Betting],
        limit: int = 100
) -> Iterator[GameStat]:
    for sample in range(30):
        random.seed(sample)
        b = Blackjack(player(), betting())
        b.until_broke_or_rounds(limit)
        yield GameStat(player.__name__, bettig.__name__, b.rounds, b.betting.stake)


with (Path.cwd() / "data").open("w", newline="") as target:
    writer = csv.DictWriter(target, GameStat._fields)
    writer.writeheader()
    for gamestat in gamestat_iter(Player_Strategy, Martingale_Bet):
        writer.writerow(gamestat._asdict())
