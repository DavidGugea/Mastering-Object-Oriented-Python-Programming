from Access3 import Access
from pathlib import Path


class Access4(Access3):
    def new(self, path: Path) -> None:
        super().new(Path)

    def create_blog(self, blog):
        super().create_blog(blog)
        blog_title_dict = self.database["_Index:Blog_Title"]
        blog_title_dict.setdefault(blog.title, [])
        blog_title_dict[blog.title].append(blog._id)
        self.database["_Index:Blog_Title"] = blog_title_dict

        return blog
