from Hand import Hand
from DominoBoneYard import DominoBoneYard
from typing import Iterator


class FancyDealer:
    def __init__(self) -> None:
        self.boneyard = DominoBoneYard()

    def hand_iter(self, players: int, tiles: int) -> Iterator[Hand]:
        if players * tiles > len(self.boneyard._dominoes):
            raise ValueError(f"Can't deal players={players} tiles={tiles}")

        for p in range(players):
            hand = Hand(self.boneyard._dominoes[:tiles])
            self.boneyard._dominoes = self.boneyard._dominoes[tiles:]
            yield hand
