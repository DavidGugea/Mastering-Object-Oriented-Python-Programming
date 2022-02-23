from Access import Access
from Blog import Blog
from Post import Post
from typing import Iterator


class Access2(Access):
    def create_post(self, blog: Blog, post: Post) -> Post:
        super().create_post(blog, post)
        # Update the index; append doesn't work.
        blog_index = f"_Index:{blog._id}"
        self.database.setdefault(blog_index, [])
        self.database[blog_index] = self.database[blog_index] + [post._id]

        return post

    def delete_post(self, post: Post) -> None:
        super().delete_post(post)

        # Update the index.
        index_list = self.database[post._blog_id]
        index_list.remove(post._id)
        self.database[post._blog_id] = index_list

    def post_iter(self, blog: Blog) -> Iterator[Post]:
        blog_index = f"_Index:{blog._id}"
        for k in self.database[blog_index]:
            yield self.database[k]
