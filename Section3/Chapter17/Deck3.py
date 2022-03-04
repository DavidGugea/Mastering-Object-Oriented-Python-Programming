import random
from Suit import Suit
from typing import Callable
from Card import Card
from CardFactory import card
from DeckEmpty import DeckEmpty


class Deck3(list):
    def __init__(
            self,
            size: int = 1,
            random: random.Random = random.Random(),
            card_factory: Callable[[int, Suit], Card] = card
    ) -> None:
        super().__init__()

        self.rng = random
        for d in range(size):
            super().extend(
                [
                    card_factory(r, s)
                    for r in range(1, 14)
                    for s in iter(Suit)
                ]
            )

        self.rng.shuffle(self)

    def deal(self) -> Card:
        try:
            return self.pop(0)
        except IndexError:
            raise DeckEmpty()
