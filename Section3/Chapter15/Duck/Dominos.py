from typing import NamedTuple
from dataclasses import dataclass


class Domino_1(NamedTuple):
    v1: int
    v2: int

    @property
    def double(self) -> bool:
        return self.v1 == self.v2


@dataclass(frozen=True, eq=True, order=True)
class Domino_2():
    v1: int
    v2: int

    @property
    def double(self) -> bool:
        return self.v1 == self.v2


