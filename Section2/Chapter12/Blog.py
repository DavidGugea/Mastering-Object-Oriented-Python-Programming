from dataclasses import dataclass, field
from typing import List
from Post import Post


@dataclass
class Blog:
    title: str
    entries: List[Post] = field(default_factory=list)
    underline: str = field(init=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)
