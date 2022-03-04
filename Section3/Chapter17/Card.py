from Suit import Suit


class Card:
    def __init__(
        self, rank: int, suit: Suit, hard: int = None, soft: int = None
    ) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard or int(rank)
        self.soft = soft or int(rank)

    def __str__(self) -> str:
        return f"{self.rank!s}{self.suit.value!s}"
