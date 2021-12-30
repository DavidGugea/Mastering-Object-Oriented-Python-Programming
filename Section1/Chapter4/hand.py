from typing import List, Tuple
import random
from enum import Enum


class BlackJackCard:
    pass


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Deck:
    """Wrapping a collection class"""

    def __init__(self) -> None:
        self._cards = [Card(r + 1, s) for r in range(13) for s in iter(Suit)]
        random.shuffle(self._cards)

    def pop(self) -> Card:
        return self._cards.pop()


class Hand:
    def __init__(
            self,
            dealer_card: BlackJackCard,
            *cards: BlackJackCard
    ) -> None:
        self.dealer_card = dealer_card
        self._cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.card))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.dealer_card!r}"
            f"{', '.join(map(str(repr, self.card)))})"
        )


class Hand_Lazy(Hand):
    @property
    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self._cards)
        hard_total = sum(c.hard for c in self._cards)
        if hard_total + delta_soft <= 21:
            return hard_total + delta_soft

        return hard_total

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, a_card: BlackJackCard) -> None:
        self._cards.append(a_card)

    @card.deleter
    def card(self) -> None:
        self._cards.pop(-1)


class Hand_Eager(Hand):
    def __init__(
            self,
            dealer_card: BlackJackCard,
            *cards: BlackJackCard
    ) -> None:
        self.dealer_card = dealer_card
        self.total = 0
        self._delta_soft = 0
        self._hard_total = 0
        self._cards: List[BlackJackCard] = list()
        for c in cards:
            self.card = c

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, a_card: BlackJackCard) -> None:
        self._cards.append(a_card)
        self._delta_soft = max(a_card.soft - a_card.hard, self._delta_soft)
        self._hard_total = self._hard_total + a_card.hard
        self._set_total()

    @card.deleter
    def card(self) -> None:
        removed = self._cards.pop(-1)
        self.hard_total -= removed.hard
        self._delta_soft = max(c.soft - c.hard for c in self._cards)
        self._set_total()

    def _set_total(self) -> None:
        if self._hard_total + self._delta_soft <= 21:
            self.total = self._hard_total + self._delta_soft
        else:
            self.total = self._hard_total


if __name__ == '__main__':
    d = Deck()
    h = Hand_Lazy(d.pop(), d.pop(), d.pop())
    print(h.total)
    h.card = d.pop()
    print(h.total)
