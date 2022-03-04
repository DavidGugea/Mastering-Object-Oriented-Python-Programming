import unittest
import unittest.mock
import random
from DeckEmpty import DeckEmpty
from Deck3 import Deck3


class TestDeckDeal(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_deck = [
            getattr(unittest.mock.sentinel, str(x)) for x in range(52)
        ]
        self.mock_card = unittest.mock.Mock(side_effect=self.mock_deck)
        self.mock_rng = unittest.mock.Mock(wraps=random.Random())
        self.mock_rng.shuffle = unittest.mock.Mock()

    def test_Deck3_should_deal(self) -> None:
        d = Deck3(size=1, random=self.mock_rng, card_factory=self.mock_card)
        dealt = []

        for i in range(52):
            card = d.deal()
            dealt.append(card)

        self.assertEqual(dealt, self.mock_deck)

    def test_empty_deck_should_exception(self) -> None:
        d = Deck3(size=1, random=self.mock_rng, card_factory=self.mock_card)
        for i in range(52):
            card = d.deal()

        self.assertRaises(DeckEmpty, d.deal)
