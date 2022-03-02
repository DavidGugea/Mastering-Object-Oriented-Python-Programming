import random
from Dominos import Domino_1, Domino_2
from typing import Type, List


class DominoBoneYard:
    domino_class: Type[Domino] = Domino_1

    def __init__(self, limit: int = 6) -> None:
        self._dominoes: List[Domino] = [
            self.domino_class(x, y)
            for x in range(limit + 1)
                for y in range(x + 1)
        ]

        random.shuffle(self._dominoes)