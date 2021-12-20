from typing import List, Union, Optional, overload
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


class Hand3:
    @overload
    def __init__(self, arg1: "Hand3") -> None:
        pass

    @overload
    def __init__(self, arg1: Card, arg2: Card, arg3: Card) -> None:
        pass

    @overload
    def __init__(
            self,
            arg1: Union[Card, "Hand3"],
            arg2: Optional[Card] = None,
            arg3: Optional[Card] = None
    ) -> None:
        self.dealer_card: Card
        self.cards: List[Card]

        if isinstance(arg1, Hand3) and not arg2 and not arg3:
            # Clone an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = arg1.cards
        elif (
                isinstance(arg1, Card) and
                isinstance(arg2, Card) and
                isinstance(arg3, Card)
        ):
            # Build a fresh, new hand.
            self.dealer_card = arg1
            self.cards = [arg2, arg3]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.dealer_card!r}, *{self.cards})"


class Hand4:
    @overload
    def __init__(self, arg1: "Hand4") -> None:
        pass

    @overload
    def __init__(self, arg1: "Hand4", arg2: Card, *, split: Card) -> None:
        pass

    @overload
    def __init__(
            self,
            arg1: Union["Hand4", Card],
            arg2: Optional[Card] = None,
            arg3: Optional[Card] = None,
            arg4: Optional[int] = None
    ) -> None:
        self.dealer_card: Card
        self.cards: List[Card]

        if isinstance(arg1, Hand4):
            # Clone an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = arg1.cards
        elif isinstance(arg1, Hand4) and isinstance(arg2, Card) and "split" is not None:
            # Split an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = [arg1.cards[split], arg2]
        elif (
                isinstance(arg1, Card) and
                isinstance(arg2, Card) and
                isinstance(arg3, Card)
        ):
            # Build a fresh, new hand  from three cards
            self.dealer_card = arg1
            self.cards = [arg2, arg3]
        else:
            raise TypeError("Invalid constructor {arg1!r} {arg2!r} {arg3!r}")

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))


class Hand5:
    def __init__(self, dealer_card: Card, *cards:Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    @staticmethod
    def freeze(other) -> "Hand5":
        hand = Hand5(other.dealer_card, *other.cards)
        return hand

    @staticmethod
    def split(other, card0, card1) -> Tuple["Hand5", "Hand5"]:
        hand0 = Hand5(other.dealer_card, other.cards[0], card0)
        hand1 = Hand5(other.dealer_card, other.cards[1], card1)
        return hand0, hand1

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))