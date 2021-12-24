from enum import Enum
import sys
from typing import Any, cast


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Card2:
    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (suit={self.suit!r}, rank={self.rank!r})"

    def __bytes__(self) -> bytes:
        class_code = self.__class__.__name__[0]
        rank_number_str = {
            "A": "1",
            "J": "11",
            "Q": "12",
            "K": "13"
        }.get(
            self.rank, str(self.rank)
        )

        string = f"({' '.join([class_code, rank_number_str, self.suit])})"
        return bytes(string, encoding="utf-8")


if __name__ == '__main__':
    card = Card2(1, Suit.Club, 11, 11)
    print(bytes(card))