from contextlib import closing
from pathlib import Path
from Access import Access
from Blog import Blog
from Post import Post
import datetime

if __name__ == '__main__':
    b1 = Blog(title="Travel Blog")
    p1 = Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Test Title",
        rst_text="""Rst Text Test""",
        tags=("tag1", "tag2", "tag3")
    )
    p2 = Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Test Title",
        rst_text="""Rst Text Test""",
        tags=("tag1", "tag2", "tag3")
    )

    path = Path.cwd() / "data" / "blog.db"

    with closing(Access()) as access:
        access.new(path)

        # Create Example
        access.create_blog(b1)
        for post in p1, p2:
            access.create_post(b1, post)

        # Retrieve Example
        b = access.retrieve_blog(b1._id)
        print(b._id, b)
        for p in access.post_iter(b):
            print(p._id, p)
