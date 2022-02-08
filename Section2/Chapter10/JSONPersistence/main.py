import datetime
import json
from BlogEncoder import blog_encode
from BlogDecoder import blog_decode
from Blog import Blog_x
from Post import Post

travel_x = Blog_x("Travel")
travel_x.append(
    Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Test Title 1",
        rst_text="""some text""",
        tags=["#test", "#this_is_a_tag"]
    )
)
travel_x.append(
    Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Test Title 2",
        rst_text="""some text 2""",
        tags=["#test2", "#this_is_a_tag_2"]
    )
)

text = json.dumps(travel_x, indent=4, default=blog_encode)
print(text)
blog_data = json.loads(text, object_hook=blog_decode)
print(blog_data)