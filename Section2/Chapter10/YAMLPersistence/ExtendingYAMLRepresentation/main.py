from enum import Enum
from typing import Optional, Any
import yaml


class Suit(str, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


class Card:
    def __init__(
        self,
        rank: str,
        suit: Suit,
        hard: Optional[int] = None,
        soft: Optional[int] = None,
    ) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __str__(self) -> str:
        return f"{self.rank!s}{self.suit.value!s}"


class AceCard(Card):
    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 1, 11)


class FaceCard(Card):
    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)


def card_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar("!Card", f"{card.rank!s}{card.suit.value!s}")


def acecard_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar("!AceCard", f"{card.rank!s}{card.suit.value!s}")


def facecard_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar("!FaceCard", f"{card.rank!s}{card.suit.value!s}")


yaml.add_representer(Card, card_representer)
yaml.add_representer(AceCard, acecard_representer)
yaml.add_representer(FaceCard, facecard_representer)


def card_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return Card(rank, suit)


def acecard_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return AceCard(rank, suit)


def facecard_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return FaceCard(rank, suit)


yaml.add_constructor("!Card", card_constructor)
yaml.add_constructor("!AceCard", acecard_constructor)
yaml.add_constructor("!FaceCard", facecard_constructor)

if __name__ == "__main__":
    deck = [
        AceCard("A", Suit.Clubs),
        Card("2", Suit.Hearts),
        FaceCard("K", Suit.Diamonds),
    ]
    text = yaml.dump(deck, allow_unicode=True)
    print(text)
    print(yaml.load(text, Loader=yaml.Loader))
