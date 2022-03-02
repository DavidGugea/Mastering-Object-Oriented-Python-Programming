import random
from Domino import Domino
from Hand import Hand
from typing import Iterator, Type


class DominoBoneYard:
    domino_class: Type[Domino] = Domino
    hand_class: Type[Hand] = Hand
    hand_size: int = 7

    def __init(self, limit: int = 6) -> None:
        self._dominoes = [self.domino_class(x, y) for x in range(limit + 1) for y in range(x + 1)]
        random.shuffle(self._dominoes)

    def hand_iter(self, players: int = 4) -> Iterator[Hand]:
        for p in range(players):
            hand = self.hand_class(self._dominoes[:self.hand_size])
            self._dominoes = self._dominoes[self.hand_size:]

            yield hand
