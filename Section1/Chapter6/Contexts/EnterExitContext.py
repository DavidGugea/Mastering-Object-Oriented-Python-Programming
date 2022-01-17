import random
from typing import Optional, Type
from types import TracebackType


class KnownSequence:
    def __init__(self, seed: int = 0) -> None:
        self.seed = seed

    def __enter__(self) -> 'KnownSequence':
        self.was = random.getstate()
        random.seed(self.seed, version=1)
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        random.setstate(self.was)
        return False
