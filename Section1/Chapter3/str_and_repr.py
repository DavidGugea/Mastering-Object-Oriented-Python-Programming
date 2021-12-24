from typing import Tuple


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (suit = {self.suit!r}, rank = {self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)


class AceCard(Card):
    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):
    def _points(self) -> Tuple[int, int]:
        return 10, 10


class Hand:
    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __repr__(self) -> str:
        cards_text = ", ".join(map(repr, self.cards))
        return f"{self.__class__.__name__} ({self.dealer_card!r}, {cards_text})"


if __name__ == '__main__':
    x = Card("2", "♠")
    print(str(x))
    print(repr(x))
    print(x)  # print uses __str__()
