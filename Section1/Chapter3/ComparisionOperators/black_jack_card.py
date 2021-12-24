from enum import Enum
from typing import Any, cast


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class BlackJackCard_p:
    def __init__(self, rank: int, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __lt__(self, other: Any) -> bool:
        print(f"Compare {self} < {other}")

        return self.rank < cast(BlackJackCard_p, other).rank

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


if __name__ == '__main__':
    two = BlackJackCard_p(2, Suit.Spade)
    three = BlackJackCard_p(3, Suit.Spade)

    print(two < three)
    print("----------")
    print(two > three)
    print("----------")
    print(two == three)
