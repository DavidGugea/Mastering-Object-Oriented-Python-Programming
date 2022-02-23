import datetime
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]
    underline: str = field(init=False)
    tag_text: str = field(init=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, repr=False, compare=False)
    _blog_id: str = field(default="", init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "-" * len(self.title)
        self.tag_text = " ".join(self.tags)
