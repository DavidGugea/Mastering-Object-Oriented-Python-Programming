from dataclasses import dataclass, field
from typing import List
from Post import Post
import datetime


@dataclass
class Blog:
    title: str
    entries: List[Post] = field(default_factory=list)
    underline: str = field(init=False, compare=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)


if __name__ == "__main__":
    import shelve
    from pathlib import Path

    b1 = Blog(title="Travel Blog")
    p1 = Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Test Title",
        rst_text="""Rst Text Test""",
        tags=("tag1", "tag2", "tag3"),
    )
    p2 = Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Test Title",
        rst_text="""Rst Text Test""",
        tags=("tag1", "tag2", "tag3"),
    )

    shelf = shelve.open(str(Path.cwd() / "data" / "Blog.dat"))
    owner = shelf["Blog:1"]

    p1._blog_id = owner._id
    p1._id = p1._blog_id + ":Post:1"
    shelf[p1._id] = p1

    p2._blog_id = owner._id
    p2._id = p2._blog_id + ":Post:2"
    shelf[p2._id] = p2

    print(list(shelf.keys()))
