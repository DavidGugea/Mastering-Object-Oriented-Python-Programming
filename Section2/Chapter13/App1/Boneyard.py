from dataclasses import dataclass, asdict, astuple
from typing import List, Dict, Any, Tuple, NamedTuple
from Domino import Domino
import random


class Boneyard:
    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [
            Domino(x, y) for x in range(0, limit + 1) for y in range(0, x + 1)
        ]
        random.shuffle(self._dominoes)

    def deal(self, tiles: int = 7, hands: int = 4) -> List[List[Domino]]:
        if tiles * hands > len(self._dominoes):
            raise ValueError(f"tiles = {tiles}, hands = {hands}")

        return [self._dominoes[h:h + tiles] for h in range(0, tiles * hands, tiles)]
