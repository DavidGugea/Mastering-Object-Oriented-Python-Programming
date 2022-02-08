from typing import Dict, Any
import datetime
from Blog import Blog_x
from Post import Post


def blog_decode(some_dict: Dict[str, Any]) -> Dict[str, Any]:
    if set(some_dict.keys()) == {"__class__", "__args__", "__kw__"}:
        class_ = eval(some_dict["__class__"])
        return class_(*some_dict["__args__"], **some_dict["__kw__"])
    else:
        return some_dict
