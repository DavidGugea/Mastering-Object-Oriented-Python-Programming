import datetime
from pathlib import Path
import json
from BlogEncoder import blog_encode_2
from Blog import Blog
from Post import Post

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

with Path("temp.json").open("w", encoding="UTF-8") as target:
    json.dump(travel, target, default=blog_encode_2)
