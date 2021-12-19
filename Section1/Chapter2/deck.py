import random
from card import *
from suit import Suit


class Deck:
    """Wrapping a collection class"""

    def __init__(self) -> None:
        self._cards = [card(r + 1, s) for r in range(13) for s in iter(Suit)]
        random.shuffle(self._cards)

    def pop(self) -> Card:
        return self._cards.pop()


class Deck2(list):
    """Extending a collection class"""

    def __init__(self) -> None:
        super().__init__(
            card(r + 1, s)
            for r in range(13) for s in iter(Suit)
        )
        random.shuffle(self)


class Deck3(list):
    """More requirements and another design"""

    def __init__(self, decks: int = 1) -> None:
        super().__init__()
        for i in range(decks):
            self.extend(
                card(r + 1, s)
                for r in range(13) for s in iter(Suit)
            )

        random.shuffle(self)
        burn = random.randint(1, 32)
        for i in range(burn):
            self.pop()


if __name__ == '__main__':
    d = Deck3()
    hand = [d.pop(), d.pop()]
