from Card import Card
from Suit import Suit


class AceCard(Card):
    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, 1, 11)
