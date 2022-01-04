from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Card:
    rank: int
    suit: str

    @property
    def points(self) -> int:
        return self.rank


class Ace(Card):
    @property
    def points(self) -> int:
        return 1


class FaceCard(Card):
    @property
    def points(self) -> int:
        return 10
