from typing import Dict, Any, Tuple, List
from dataclasses import dataclass, asdict
import random
import secrets
from Status import Status


@dataclass
class Dice:
    roll: List[int]
    identifier: str
    status: str

    def reroll(self, keep_positions: List[int]) -> None:
        for i in range(len(self.roll)):
            if i not in keep_positions:
                self.roll[i] = random.randint(1, 6)

        self.status = Status.UPDATED


def make_dice(n_dice: int) -> Dice:
    return Dice(
        roll=[random.randint(1, 6) for _ in range(n_dice)],
        identifier=secrets.token_urlsafe(8),
        status=Status.CREATED
    )
