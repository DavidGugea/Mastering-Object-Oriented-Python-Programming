import logging


class Player:
    def __init__(self, bet: str, strategy: str, stake: int) -> None:
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.logger.debug(f"init bet {bet!r}, strategy ${strategy!r}, stake ${stake!r}")