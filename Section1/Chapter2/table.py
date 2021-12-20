from deck import *
from hand import *

class Table:
    def __init__(self) -> None:
        self.deck = Deck()

    def place_bet(self, amount: int) -> None:
        print("Bet {0}".format(amount))

    def get_hand(self) -> Hand2:
        try:
            self.hand = Hand2(
                self.deck.pop(), self.deck.pop(), self.deck.pop()
            )
            self.hole_card = self.deck.pop()
        except IndexError:
            # Out of cards: need to shuffle and try again
            self.deck = Deck()
            return self.get_hand()

        print("Deal {0}".format(self.hand))
        return self.hand

    def can_insure(self, hand: Hand) -> bool:
        return hand.dealer_card.insure