import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str] = field(default_factory=list)
    _id: str = field(default="", init=False, compare=False)

    def append(self, tag) -> None:
        self.tag.append(tag)
