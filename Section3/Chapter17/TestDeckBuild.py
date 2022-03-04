import random
import unittest
import unittest.mock
from Suit import Suit
from Deck3 import Deck3


class TestDeckBuild(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_card = unittest.mock.Mock(return_value=unittest.mock.sentinel.card)
        self.mock_rng = unittest.mock.Mock(wraps=random.Random())
        self.mock_rng.shuffle = unittest.mock.Mock()

    def test_Deck3_should_build(self) -> None:
        d = Deck3(size=1, random=self.mock_rng, card_factory=self.mock_card)

        self.assertEqual(52 * [unittest.mock.sentinel.card], d)
        self.mock_rng.shuffle.assert_called_with(d)
        self.assertEqual(52, len(self.mock_card.mock_calls))
        expected = [
            unittest.mock.call(r, s)
            for r in range(1, 14)
            for s in (Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE)
        ]

        self.assertEqual(expected, self.mock_card.mock_calls)