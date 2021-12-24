from enum import Enum
import sys
from typing import Any, cast


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Card:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (suit={self.suit!r}, rank={self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class FaceCard(Card):
    def __init__(self, rank: int, suit: "Suit") -> None:
        rank_str = {
            11: "J",
            12: "Q",
            13: "K"
        }[rank]
        super().__init__(rank_str, suit, 10, 10)


class Card2:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (suit={self.suit!r}, rank={self.rank!r})"


class Card3:
    insure = False

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __eq__(self, other: Any) -> bool:
        return (
                self.suit == cast(Card2, other).suit
                and self.rank == cast(Card2, other).rank
        )

    def __hash__(self) -> int:
        return (hash(self.suit) + 4 * hash(self.rank)) % sys.hash_info.modulus


class AceCard(Card2):
    insure = True

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__("A", suit, 1, 11)


class Card3:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (suit={self.suit!r}, rank={self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __eq__(self, other: Any) -> bool:
        return (
                self.suit == cast(Card3, other).suit
                and self.rank == cast(Card3, other).rank
        )


class AceCard3(Card3):
    insure = True

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__("A", suit, 1, 11)


class Hand:
    def __init__(self, dealer_card: Card2, *cards: Card2) -> None:
        self.dealer_card = dealer_card
        self.cards = cards

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __repr__(self) -> str:
        cards_text = ", ".join(map(repr, self.cards))
        return f"{self.__class__.__name__} ({self.dealer_card!r}, {cards_text})"

    def __format__(self, format_specification: str) -> str:
        if format_specification == "":
            return str(self)

        return ", ".join(
            f"{card: {format_specification}}" for card in self.cards
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() == cast(int, other)

        try:
            return (
                    self.cards == cast(Hand, other).cards
                    and self.dealer_card == cast(Hand, other).dealer_card
            )
        except AttributeError:
            return NotImplemented


class FrozenHand(Hand):
    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1 and isinstance(args[0], Hand):
            # Clone a hand
            other = cast(Hand, args[0])
            self.dealer_card = other.dealer_card
        else:
            # Build a fresh Hand from Card instances.
            super().__init__(*args, **kwargs)

    def __hash__(self) -> int:
        return sum(hash(c) for c in self.cards) % sys.hash_info.modulus


if __name__ == '__main__':
    c1 = AceCard3(1, Suit.Club)
    c2 = AceCard3(1, Suit.Club)

    print("id   | c1 : {0:< 15} | c2 : {1}".format(id(c1), id(c2)))
    # print("hash | c1 : {0:< 15} | c2 : {1}".format(hash(c1), hash(c2)))
    print(c1 is c2)
    print(c1 == c2)
