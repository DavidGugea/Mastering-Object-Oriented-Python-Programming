import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]
    underline: str = field(init=False)
    tag_text: str = field(init=False)

    def __post_init__(self) -> None:
        self.underline = "-" * len(self.title)
        self.tag_text = " ".join(self.tags)
