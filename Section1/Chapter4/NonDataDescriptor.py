from pathlib import Path
from typing import Type, Optional


class PersistentState:
    """Abstract superclass to use a StateManager object"""
    _saved: Path


class StateManager:
    """May create a directory. Sets _saved in the instance."""

    def __init__(self, base: Path) -> None:
        self.base = base

    def __get__(self, instance: PersistentState, owner: Type) -> Path:
        if not hasattr(instance, "_saved"):
            class_path = self.base / owner.__name__
            class_path.mkdir(exist_ok=True, parents=True)
            instance._saved = class_path / str(id(instance))

        return instance._saved


class PersistenceClass(PersistentState):
    state_path = StateManager(Path.cwd() / "data" / "state")

    def __init__(self, a: int, b: float) -> None:
        self.a = a
        self.b = b
        self.c: Optional[float] = None
        self.state_path.write_text(repr(vars(self)))

    def calculate(self, c: float) -> float:
        self.c = c
        self.state_path.write_text(repr(vars(self)))
        return self.a * self.b * self.c

    def __str__(self) -> str:
        return self.state_path.read_text()


if __name__ == '__main__':
    x = PersistenceClass(1, 2)
    print(str(x))
    x.calculate(3)
    print(str(x))
