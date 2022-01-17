from pathlib import Path
from typing import Optional, Type
from types import TracebackType


class Updating:
    def __init__(self, target: Path) -> None:
        self.target: Path = target
        self.previous: Optional[Path] = None

    def __enter__(self) -> None:
        try:
            self.previous = (
                    self.target.parent
                    / (self.target.stem + " backup")
            ).with_suffix(self.target.suffix)
            self.target.rename(self.previous)
        except FileNotFoundError:
            self.previous = None

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        if exc_type is not None:
            try:
                self.failure = (
                        self.target.parent
                        / (self.target.stem + " error")
                ).with_suffix(self.target.suffix)
                self.target.rename(self.failure)
            except FileNotFoundError:
                pass
            if self.previous:
                self.previous.rename(self.target)

        return False
