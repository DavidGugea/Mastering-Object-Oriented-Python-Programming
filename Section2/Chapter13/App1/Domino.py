from dataclasses import dataclass


@dataclass(frozen=True)
class Domino:
    v_0: int
    v_1: int

    @property
    def double(self) -> bool:
        return self.v_0 == self.v_1

    def __repr__(self) -> str:
        if self.double:
            return f"Double({self.v_0})"
        else:
            return f"Domino({self.v_0}, {self.v_1})"
