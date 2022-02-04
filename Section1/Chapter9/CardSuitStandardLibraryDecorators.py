from typing import Any, cast
from enum import Enum
import functools


class Suit(Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


@functools.total_ordering
class CardTO:
    __slots__ = ("rank", "suit")

    def __init__(self, rank: int, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __eq__(self, other: Any) -> bool:
        return self.rank == cast(CardTO, other).rank

    def __lt__(self, other: Any) -> bool:
        return self.rank < cast(CardTO, other).rank

    def __str__(self) -> str:
        return f"{self.rank:d}{self.suit:s}"
