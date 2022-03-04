import unittest
from Suit import Suit
from CardFactory import card
from Card import Card
from AceCard import AceCard
from LogicError import LogicError


class TestCardFactory(unittest.TestCase):
    def test_rank1_should_createAceCard(self) -> None:
        c = card(1, Suit.CLUB)
        self.assertIsInstance(c, AceCard)

    def test_rank2_should_createCard(self) -> None:
        c = card(2, Suit.DIAMOND)
        self.assertIsInstance(c, Card)

    def test_rank10_should_createCard(self) -> None:
        c = card(10, Suit.HEART)
        self.assertIsInstance(c, Card)

    def test_rank10_should_createFaceCard(self) -> None:
        c = card(11, Suit.SPADE)
        self.assertIsInstance(c, Card)

    def test_rank13_should_createFaceCard(self) -> None:
        c = card(13, Suit.CLUB)
        self.assertIsInstance(c, Card)

    def test_otherRank_should_exception(self) -> None:
        with self.assertRaises(LogicError):
            c = card(14, Suit.DIAMOND)

        with self.assertRaises(LogicError):
            c = card(0, Suit.DIAMOND)
