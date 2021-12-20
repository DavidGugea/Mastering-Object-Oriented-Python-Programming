from hand import *
from abc import abstractmethod, ABCMeta


class GameStrategy:
    """Stateless class without __init__()"""

    def insurance(self, hand: Hand) -> bool:
        return False

    def split(self, hand: Hand) -> bool:
        return False

    def double(self, hand: Hand) -> bool:
        return False

    def hit(self, hand: Hand) -> bool:
        return sum(c.hard for c in hand.cards) <= 17


class BettingStrategy:
    def bet(self) -> int:
        raise NotImplementedError("No bet method")

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass


class Flat(BettingStrategy):
    def bet(self) -> int:
        return 1


class BettingStrategy2(metaclass=ABCMeta):
    @abstractmethod
    def bet(self) -> int:
        return 1

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass
