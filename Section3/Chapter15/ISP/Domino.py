from typing import NamedTuple


class Domino(NamedTuple):
    v1: int
    v2: int

    def double(self) -> bool:
        return self.v1 == self.v2

    def score(self) -> int:
        return self.v1 + self.v2