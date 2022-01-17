class BettingStrategy:
    def __init__(self) -> None:
        self.win = 0
        self.loss = 0

    def __call__(self) -> int:
        return 1


class BettingMartingale(BettingStrategy):
    def __init__(self) -> None:
        self.win = 0
        self._loss = 0
        self.stage = 1

    @property
    def win(self) -> int:
        return self._win

    @win.setter
    def win(self, value: int) -> None:
        self._win = value
        self.stage = 1

    @property
    def loss(self) -> int:
        return self._loss

    @loss.setter
    def loss(self, value: int) -> None:
        self._loss = value
        self.stage *= 2

    def __call__(self) -> int:
        return self.stage


class BettingMartingale2(BettingStrategy):
    """Only implementing __setattr__ since we are only interested in the setters; we'll never use the getters."""
    def __init__(self) -> None:
        self.win = 0
        self.loss = 0
        self.stage = 1

    def __setattr__(self, name: str, value: int) -> None:
        if name == "win":
            self.stage = 1
        elif name == "loss":
            self.stage *= 2

        super().__setattr__(name, value)

    def __call__(self) -> None:
        return self.stage