from enum import Enum
from typing import Optional, Dict, Any
import pickle
import logging, sys

audit_log = logging.getLogger("audit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class Suit(str, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


class Card:
    def __init__(self, rank: str, suit: Suit,
                 hard: Optional[int] = None,
                 soft: Optional[int] = None) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft


class AceCard(Card):
    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 1, 11)


class FaceCard(Card):
    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)


class Hand_bad:
    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)
        for c in self.cards:
            audit_log.info("Initial {0}".format(c))

    def append(self, card: Card) -> None:
        self.cards.append(card)
        audit_log.info("Hit %s", card)

    def __str__(self) -> str:
        cards = ", ".join(map(str, self.cards))
        return f"{self.dealer_card} | {cards}"

class Hand2:
    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)
        for c in self.cards:
            audit_log.info("Initial {0}".format(c))

    def append(self, card: Card) -> None:
        self.cards.append(card)
        audit_log.info("Hit %s", card)

    def __str__(self) -> str:
        cards = ", ".join(map(str, self.cards))
        return f"{self.dealer_card} | {cards}"

    def __getstate__(self) -> Dict[str, Any]:
        return vars(self)

    def __setstate__(self, state: Dict[str, Any]) -> None:
        # Not very secure -- hard for mypy to detect what's going on
        self.__dict__.update(state)
        for c in self.cards:
            audit_log.info("Initial (unpickle) {0}".format(c))


if __name__ == '__main__':
    h = Hand2(
        FaceCard("K", "♦"),
        AceCard("A", "♠"),
        Card("9", "♥")
    )
    data = pickle.dumps(h)
    print(data)
    h2 = pickle.loads(data)
    print(h2)
