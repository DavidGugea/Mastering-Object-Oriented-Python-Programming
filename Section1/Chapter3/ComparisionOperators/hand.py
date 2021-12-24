from enum import Enum
from typing import Any, cast


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Card2:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (suit={self.suit!r}, rank={self.rank!r})"


class Hand:
    def __init__(self, dealer_card: Card2, *cards: Card2) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __repr__(self) -> str:
        cards_text = ", ".join(map(repr, self.cards))
        return f"{self.__class__.__name__} ({self.dealer_card!r}, {cards_text})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() == other

        try:
            return (
                    self.cards == cast(Hand, other).cards
                    and self.dealer_card == cast(Hand, other).dealer_card
            )
        except AttributeError:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() < cast(int, other)

        try:
            return self.total() < cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() <= cast(int, other)

        try:
            return self.total() <= cast(int, other)
        except AttributeError:
            return NotImplemented

    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self.cards)
        hard = sum(c.hard for c in self.cards)
        if hard + delta_soft <= 21:
            return hard + delta_soft

        return hard
