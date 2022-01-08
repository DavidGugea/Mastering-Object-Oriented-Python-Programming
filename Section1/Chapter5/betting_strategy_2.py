from abc import ABC, abstractmethod
from hand import Hand


class AbstractBettingStrategy2(ABC):
    @abstractmethod
    def bet(self, hand: Hand) -> int:
        return 1

    @abstractmethod
    def record_win(self, hand: Hand) -> None:
        pass

    @abstractmethod
    def record_loss(self, hand: Hand) -> None:
        pass

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        """Validate if the class definition is complete."""
        if cls is AbstractBettingStrategy2:
            has_bet = any(hasattr(B, "bet") for B in subclass.__mro__)
            has_record_win = any(hasattr(B, "record_win") for B in subclass.__mro__)
            has_record_loss = any(hasattr(B, "record_loss") for B in subclass.__mro__)

            if has_bet and has_record_win and has_record_loss:
                return True

            return False
