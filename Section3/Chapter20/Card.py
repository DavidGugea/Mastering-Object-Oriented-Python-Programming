from Suit import Suit
from typing import Optional


class Card:
    """
    Definition of a numeric rank playing card.
    Subclasses will define :py:class:`FaceCard` and :py:class:`AceCard`.

    :ivar rank: int rank of the card
    :ivar suit: Suit suit of the card
    :ivar hard: int Hard point total for a card
    :ivar soft: int Soft total; same as hard for all cards except Aces.
    """

    def __init__(
            self, rank: int, suit: Suit, hard: int, soft: Optional[int] = None
    ) -> None:
        """ Define the values for this card.

        :param rank:  Numeric rank in the range 1-13.
        :param suit:  Suit object from :class:`Suits`
        :param hard:  Hard point total ( or 10 for FaceCard or 1 for AceCard )
        :param soft:  The soft total for AceCArd, otherwise defaults to hard.
        """

        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit})"


def card(rank: int, suit: Suit) -> Card:
    """
    Create a :py:class:`Card` instance from rank and suit.

    :param rank:  Suit object
    :param suit:  Numeric rank in the range-13
    :returns:  :py:class:`Card` instance
    :raises TypeError:    rank out of range


    >>> str(card(3, Suit.Heart))
    '3♥'
    >>> str(card(1, Suit.Heart))
    'A♥'
    """

    if rank == 1:
        return AceCard(rank, suit, 1, 11)
    elif 2 <= rank < 11:
        return Card(rank, suit, rank)
    elif 11 <= rank < 14:
        return FaceCard(rank, suit, 10)
    else:
        raise TypeError
