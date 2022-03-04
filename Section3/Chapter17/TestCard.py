import unittest
from Card import Card
from Suit import Suit


class TestCard(unittest.TestCase):
    def setUp(self) -> None:
        self.three_clubs = Card(3, Suit.CLUB)

    def test_should_returnStr(self) -> None:
        self.assertEqual("3♣", str(self.three_clubs))

    def test_should_getAttrValues(self) -> None:
        self.assertEqual(3, self.three_clubs.rank)
        self.assertEqual(Suit.CLUB, self.three_clubs.suit)
        self.assertEqual(3, self.three_clubs.hard)
        self.assertEqual(3, self.three_clubs.soft)
