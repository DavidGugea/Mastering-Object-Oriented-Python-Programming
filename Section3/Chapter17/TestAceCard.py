import unittest
from AceCard import AceCard
from Suit import Suit


class TestAceCard(unittest.TestCase):
    def setUp(self) -> None:
        self.ace_spades = AceCard(1, Suit.SPADE)

    @unittest.expectedFailure
    def test_should_returnStr(self) -> None:
        self.assertEqual("A♠", str(self.ace_spades))

    def test_should_getAttrValues(self) -> None:
        self.assertEqual(1, self.ace_spades.rank)
        self.assertEqual(Suit.SPADE, self.ace_spades.suit)
        self.assertEqual(1, self.ace_spades.hard)
        self.assertEqual(11, self.ace_spades.soft)
