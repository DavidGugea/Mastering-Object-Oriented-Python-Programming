import datetime
from Blog import Blog_x
from Post import Post
from typing import Any, Dict


def blog_encode(object: Any) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        return dict(
            __class__="datetime.datetime",
            __args__=[],
            __kw__=dict(
                year=object.year,
                month=object.month,
                day=object.day,
                hour=object.hour,
                minute=object.minute,
                second=object.second
            ),
        )
    elif isinstance(object, Post):
        return dict(
            __class__="Post",
            __args__=[],
            __kw__=dict(
                date=object.date,
                title=object.title,
                rst_text=object.rst_text,
                tags=object.tags
            ),
        )
    elif isinstance(object, Blog_x):
        return dict(
            __class__="Blog",
            __args__=[object.title, object.entries],
            __kw__={}
        )
    else:
        return object
