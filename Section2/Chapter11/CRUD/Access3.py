from Access2 import Access2
from pathlib import Path
from Blog import Blog
from typing import Iterator

class Access3(Access2):
    def new(self, path: Path) -> None:
        super().new(Path)
        self.database["_Index:Blog"] = list()

    def create_blog(self, blog: Blog) -> Blog:
        super().create_blog(blog)
        self.database["_Index:Blog"] += [blog._id]
        return blog

    def blog_iter(self) -> Iterator[Blog]:
        return (self.database[k] for k in self.database["_Index:Blog"])
