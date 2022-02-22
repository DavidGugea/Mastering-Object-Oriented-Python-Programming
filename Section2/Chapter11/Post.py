from dataclasses import dataclass
import datetime
from typing import List


@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]
