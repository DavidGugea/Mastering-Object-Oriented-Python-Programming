from table import *
from strategy import *


class Player:
    def __init__(
            self,
            table: Table,
            bet_strategy: BettingStrategy,
            game_strategy: GameStrategy
    ) -> None:
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
        if self.table.can_insure(self.hand):
            if self.game_strategy.insurance(self.hand):
                self.table.insure(self.bet_strategy.bet())

        # etc.


class Player2:
    def __init__(self, **kw) -> None:
        """Must provide table, bet_strategy, game_strategy"""
        self.bet_strategy: BettingStrategy = kw["bet_strategy"]
        self.game_strategy: GameStrategy = kw["game_strategy"]
        self.table: Table = kw["table"]

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()


class Player2x:
    def __init__(self, **kw) -> None:
        """Must provide table, bet_strategy, game_strategy"""
        self.bet_strategy: BettingStrategy = kw["bet_strategy"]
        self.game_strategy: GameStrategy = kw["game_strategy"]
        self.table: Table = kw["table"]
        self.log_name: Optional[str] = kw.get("log_name")


class Player3:
    def __init__(
            self,
            table: Table,
            bet_strategy: BettingStrategy,
            game_strategy: GameStrategy,
            **extras
    ) -> None:
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table
        self.log_name: str = extras.pop("log_name", self.__class__.__name__)

        if extras:
            raise TypeError(f"Extra arguments: {extras!r}")


class ValidPlayer:
    def __init__(self, table, bet_strategy, game_strategy):
        assert isinstance(table, Table)
        assert isinstance(bet_strategy, BettingStrategy)
        assert isinstance(game_strategy, GameStrategy)

        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table


if __name__ == '__main__':
    """
    table = Table()
    flat_bet = Flat()
    dumb = GameStrategy()
    p = Player(table, flat_bet, dumb)
    p.game()
    """

    table = Table()
    flat_bet = Flat()
    dumb = GameStrategy()
    p = Player2(table=table, bet_strategy=flat_bet, game_strategy=dumb)
