from typing import Iterator, Tuple


class Table: ...


class Player: ...


class Simulate:
    def __init__(
            self,
            table: Table,
            player: Player,
            samples: int
    ):
        pass

    def __iter__(self) -> Iterator[Tuple]:
        pass
