from typing import List, Dict, Any
from dataclasses import dataclass, field, asdict
import datetime


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

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def xml(self) -> str:
        tags = "".join(f"<tag>{t}</tag>" for t in self.tags)
        return f"""\
<entry>
    <title>{self.title}</title>
    <date>{self.date}</date>
    <tags>{self.tags}</tags>
    <text>{self.rst_text}</text>
</entry>"""
