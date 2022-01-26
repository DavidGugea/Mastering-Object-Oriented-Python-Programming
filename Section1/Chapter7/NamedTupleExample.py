from typing import NamedTuple


class Suit:
    pass


class BlackjackCard_T(NamedTuple):
    rank: str
    suit: Suit
    hard: int
    soft: int


def card_t(rank: int, suit: Suit) -> BlackjackCard_T:
    if rank == 1:
        return BlackjackCard_T("A", suit, 1, 11)
    elif 2 <= rank < 11:
        return BlackjackCard_T(str(rank), suit, rank, rank)


