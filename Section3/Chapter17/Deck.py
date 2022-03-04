import random
from Suit import Suit
from Card import Card
from AceCard import AceCard
from FaceCard import FaceCard
from typing import Type


class Deck(list):
    def __init__(
        self,
        size: int = 1,
        random: random.Random = random.Random(),
        ace_class: Type[Card] = AceCard,
        card_class: Type[Card] = Card,
        face_class: Type[Card] = FaceCard,
    ) -> None:
        super().__init__()

        self.rng = random
        for d in range(size):
            for s in iter(Suit):
                cards = (
                    [ace_class(1, s)]
                    + [card_class(r, s) for r in range(2, 12)]
                    + [face_class(r, s) for r in range(12, 14)]
                )

                super().extend(cards)

        self.rng.shuffle(self)
