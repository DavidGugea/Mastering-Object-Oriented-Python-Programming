from pytest import raises
from CardFactory import card

from Card import Card
from AceCard import AceCard

from Suit import Suit

from LogicError import LogicError


def test_card_factory():
    c1 = card(1, Suit.CLUB)
    assert isinstance(c1, AceCard)

    c2 = card(2, Suit.DIAMOND)
    assert isinstance(c2, Card)

    with raises(LogicError):
        c14 = card(14, Suit.DIAMOND)

    with raises(LogicError):
        c0 = card(0, Suit.DIAMOND)
