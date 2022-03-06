from enum import Enum

__all__ = ["Deck", "Shoe"]


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦💎"
    Heart = "♥"
    Spade = "♠"


class Card: ...


def card(rank: int, suit: Suit) -> Card: ...


class Deck: ...


class Shoe(Deck): ...
