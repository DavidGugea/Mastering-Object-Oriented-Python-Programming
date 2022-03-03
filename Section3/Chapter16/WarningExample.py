import warnings


class Player:
    """version 2.1"""

    def bet(self) -> None:
        warnings.warn("bet is deprecated, use place_bet", DeprecationWarning, stacklevel=2)
        pass


if __name__ == '__main__':
    warnings.simplefilter("always", category=DeprecationWarning)
    p2 = Player()
    p2.bet()
