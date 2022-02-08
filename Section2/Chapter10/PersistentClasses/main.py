import datetime
from Blog import Blog_x
from Post import post

travel_x = Blog_x("Travel")
travel_x.append(
    Post(
        date = datetime.datetime(2013, 11, 14, 17, 25),
        title = "Test Title 1",
        rst_text = """some text""",
        tags = ["#test", "#this_is_a_tag"]
    )
)
travel_x.append(
    Post(
        date = datetime.datetime(2013, 11, 18, 15, 30),
        title = "Test Title 2",
        rst_text = """some text 2""",
        tags = ["#test2", "#this_is_a_tag_2"]
    )
)