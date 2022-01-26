from typing import Dict, List, Tuple, DefaultDict, Any
from collections import defaultdict
import random


def dice_examples(n: int = 12, seed: Any = None) -> DefaultDict[int, List]:
    if seed:
        random.seed(seed)

    Roll = Tuple[int, int]
    outcomes: DefaultDict[int, List[Roll]] = defaultdict(list)
    for _ in range(n):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        outcomes[d1 + d2].append((d1, d2))
    return outcomes