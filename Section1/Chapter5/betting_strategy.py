from abc import ABCMeta, abstractmethod
from hand import Hand


class AbstractBettingStrategy(metaclass=ABCMeta):
    @abstractmethod
    def bet(self, hand: Hand) -> int:
        return 1

    @abstractmethod
    def record_win(self, hand: Hand) -> None:
        pass

    @abstractmethod
    def record_loss(self, hand: Hand) -> None:
        pass


class Simple_Broken(AbstractBettingStrategy):
    def bet(self, hand: Hand):
        return 1


class Simple(AbstractBettingStrategy):
    def bet(self, hand: Hand) -> int:
        pass

    def record_win(self, hand: Hand) -> None:
        pass

    def record_loss(self, hand: Hand) -> None:
        pass