from typing import List
from deck import Deck
from card import *


class Hand:
    def __init__(self, dealer_card: Card) -> None:
        self.dealer_card: Card = dealer_card
        self.cards: List[Card] = []

    def hard_total(self) -> int:
        return sum(c.hard for c in self.cards)

    def soft_total(self) -> int:
        return sum(c.soft for c in self.cards)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.dealer_card} {self.cards}"


class Hand2:
    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card: Card = dealer_card
        self.cards = list(cards)

    def card_append(self, card: Card) -> None:
        self.cards.append(card)

    def hard_total(self) -> int:
        return sum(c.hard for c in self.cards)

    def soft_total(self) -> int:
        return sum(c.soft for c in self.cards)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.dealer_card!r} *{self.cards})"


if __name__ == '__main__':
    d = Deck()
    h = Hand2(d.pop(), d.pop(), d.pop())
