from LogicError import LogicError
from Card import Card
from AceCard import AceCard
from FaceCard import FaceCard
from Suit import Suit


def card(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard(rank, suit)
    elif 2 <= rank < 11:
        return Card(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard(rank, suit)
    else:
        raise LogicError(f"Rank {rank} invalid")
