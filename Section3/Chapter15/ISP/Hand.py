from Domino import Domino
from typing import cast, List, Tuple, Any


class Hand(list):
    def __init__(self, *args: List[Domino]) -> None:
        super().__init__(cast(Tuple[Any], args))

    def score(self) -> int:
        return sum(d.score() for d in self)

    def rank(self) -> None:
        self.sort(key=lambda d: d.score(), reverse=True)

    def doubles_indices(self) -> List[int]:
        return [i for i in range(len(self)) if self[i].double()]
