import random
from typing import Optional, Type
from types import TracebackType


class Deck:
    def __init__(self, *args, **kwargs):
        pass


class Deterministic_Deck:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def __enter__(self) -> Deck:
        self.was = random.getstate()
        random.seed(0, version=1)
        return Deck(*self.args, **self.kwargs)

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        random.setstate(self.was)
        return False
