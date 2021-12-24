from enum import Enum
from typing import Any, cast


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class BlackJackCard:
    def __init__(self, rank: int, suit: Suit, hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented

        return self.rank < other.rank

    def __le__(self, other: Any) -> bool:
        try:
            return self.rank <= cast(BlackJackCard, other).rank
        except AttributeError:
            return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented

        return self.rank > other.rank

    def __ge__(self, other: Any) -> bool:
        try:
            return self.rank >= cast(BlackJackCard, other).rank
        except AttributeError:
            return NotImplemented

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented

        return (
                self.rank == other.rank
                and self.suit == other.suit
        )

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented

        return (
                self.rank != other.rank
                or self.suit != other.suit
        )

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(rank={self.rank!r}, suit={self.suit!r}"
            f"hard={self.hard!r}, soft={self.soft!r})"
        )
