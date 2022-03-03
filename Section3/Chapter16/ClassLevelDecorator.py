from typing import Type
import logging


def logged(cls: Type) -> Type:
    cls.logger = logging.getLogger(cls.__qualname__)
    return cls


@logged
class Player:
    def __init__(self, bet: str, strategy: str, stake: int) -> None:
        self.logger.debug(f"init bet {bet!r}, strategy ${strategy!r}, stake ${stake!r}")
