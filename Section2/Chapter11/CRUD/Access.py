import shelve
from pathlib import Path
from typing import cast, Dict, Iterator, Union
from Blog import Blog
from Post import Post


class Access:
    def __init__(self) -> None:
        self.database: shelve.Shelf = cast(shelve.Shelf, None)
        self.max: Dict[str, int] = {"Post": 0, "Blog": 0}

    def new(self, path: Path) -> None:
        self.database = shelve.Shelf = shelve.open(str(path), "n")
        self.max: Dict[str, int] = {"Post": 0, "Blog": 0}

        self.sync()

    def open(self, path: Path) -> None:
        self.database = shelve.open(str(path), "n")
        self.max = self.database["_DB:max"]

    def close(self) -> None:
        if self.database:
            self.database["_DB:max"] = self.max
            self.database.close()

        self.database = cast(shelve.Shelf, None)

    def sync(self) -> None:
        self.database["_DB:max"] = self.max
        self.database.sync()

    def quit(self) -> None:
        self.close()

    def create_blog(self, blog: Blog) -> Blog:
        self.max["Blog"] += 1
        key = f"Blog:{self.max['Blog']}"
        blog._id = key

        ###################################
        self.database[blog._id] = blog
        ###################################

        return blog

    def retrieve_blog(self, key: str) -> Blog:
        return self.database[key]

    def create_post(self, blog: Blog, post: Post) -> Post:
        self.max["Post"] += 1
        post_key = f"Post:{self.max['Post']}"
        post._id = post_key
        post._blog_id = blog._id

        #################################
        self.database[post._id] = post
        #################################

        return post

    def retrieve_post(self, key: str) -> Post:
        return self.database[key]

    def update_post(self, post: Post) -> Post:
        self.database[post._id] = post
        return post

    def delete_post(self, post: Post) -> None:
        del self.database[post._id]

    def __iter__(self) -> Iterator[Union[Blog, Post]]:
        for k in self.database:
            if k[0] == "_":
                continue  # Skip the administrative objects
            yield self.database[k]

    def blog_iter(self) -> Iterator[Blog]:
        for k in self.database:
            if k.startswith("Blog:"):
                yield self.database[k]

    def post_iter(self, blog: Blog) -> Iterator[Post]:
        for k in self.database:
            if k.startswith("Post:"):
                if self.database[k]._blog_id == blog._id:
                    yield self.database[k]

    def post_title_iter(self, blog: Blog, title: str) -> Iterator[Post]:
        return (p for p in self.post_iter(blog) if p.title == title)
