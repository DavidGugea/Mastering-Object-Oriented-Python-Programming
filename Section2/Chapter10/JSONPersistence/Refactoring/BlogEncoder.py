import datetime
import json

from typing import Union, Dict, Any
from Blog import Blog
from Post import Post


def blog_encode_2(object: Union[Blog, Post, Any]) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        fmt = "%Y-%m-%dT%H:%M:%S"
        return dict(
            __class__="datetime.datetime.strptime",
            __args__=[object.strftime(fmt), fmt],
            __kw__={}
        )
    else:
        try:
            encoding = object._json
        except AttributeError:
            encoding = json.JSONEncoder().default(object)
        return encoding
