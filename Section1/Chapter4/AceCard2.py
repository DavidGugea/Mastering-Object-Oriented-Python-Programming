from typing import NamedTuple
from hand import Suit


class AceCard2(NamedTuple):
    rank: str
    suit: Suit
    hard: int = 1
    soft: int = 11

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


if __name__ == '__main__':
    c = AceCard2("A", Suit.Spade)
    print(c.rank)
    print(c.suit)
    print(c.hard)

    # c.not_allowed = 2 -- > AttributeError
    # c.rank = 3 -- > AttributeError