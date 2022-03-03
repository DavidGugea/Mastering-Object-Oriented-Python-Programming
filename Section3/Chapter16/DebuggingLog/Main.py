from LoggedClass import LoggedClass
from typing import Dict


class BettingStrategy(LoggedClass):
    def bet(self) -> int:
        raise NotImplementedError("No bet method")

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass


class OneThreeTwoSix(BettingStrategy):
    def __init__(self) -> None:
        self.wins = 0

    def _state(self) -> Dict[str, int]:
        return dict(wins=self.wins)

    def bet(self) -> int:
        bet = {0: 1, 1: 3, 2: 2, 3: 6}[self.wins % 4]

        self.logger.debug(f"Bet {self._state()}; based on {bet}")
        return bet

    def record_win(self) -> None:
        self.wins += 1
        self.logger.debug(f"Win: {self._state()}")

    def record_loss(self) -> None:
        self.wins = 0
        self.logger.debug(f"Loss: {self._state()}")
