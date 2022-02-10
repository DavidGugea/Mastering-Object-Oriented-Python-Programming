import datetime
from Blog import Blog
from Post import Post
from pathlib import Path
import csv

travel = Blog("Travel")
travel.append(
    Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Test Title 1",
        rst_text="""some text""",
        tags=["#test", "#this_is_a_tag"],
    )
)
travel.append(
    Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Test Title 2",
        rst_text="""some text 2""",
        tags=["#test2", "#this_is_a_tag_2"],
    )
)

with (Path.cwd() / "data").open("w", newline="") as target:
    wtr = csv.writer(target)
    wtr.writerow(["__class__", "title", "date", "title", "rst_text", "tags"])
    blogs = [travel]
    for b in blogs:
        wtr.writerow(["Blog", b.title, None, None, None, None])
        for p in b:
            wtr.writerow(["Post", p.date, p.title, p.rst_text, p.tags])
