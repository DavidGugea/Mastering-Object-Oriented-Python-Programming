from dataclasses import dataclass
from typing import Iterator, Tuple


@dataclass
class Simulate:
    """Mock Simulation."""

    table: Table
    player: Player
    samples: int

    def __iter__(self) -> Iterator[Tuple]:
        """Yield statistical samples."""
        # Processing goes here...
        pass
