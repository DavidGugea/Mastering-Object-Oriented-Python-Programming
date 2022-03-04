from Card import Card
from Suit import Suit


class FaceCard(Card):
    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)
