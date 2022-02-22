from dataclasses import dataclass, asdict, field
from typing import List
from Post import Post


@dataclass
class Blog:
    title: str
    entries: List[Post] = field(default_factory=list)
    underline: str = field(init=False, compare=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)


if __name__ == '__main__':
    import shelve
    from pathlib import Path

    b1 = Blog(title="Travel Blog")
    shelf = shelve.open(str(Path.cwd() / "data" / "Blog.dat"))

    b1._id = "Blog:1"
    shelf[b1._id] = b1