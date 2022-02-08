from typing import DefaultDict, List, Dict, Any, Optional
from Post import Post
from collections import defaultdict


class Blog(list):
    def __init__(self, title: str, posts: Optional[List[Post]] = None) -> None:
        self.title = title
        super().__init__(posts if posts is not None else [])

    def by_tag(self) -> DefaultDict[str, List[Dict[str, Any]]]:
        tag_index: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in self:
            for tag in post.tags:
                tag_index[tag].append(post.as_dict())

        return tag_index

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            title=self.title,
            entries=[p.as_dict() for p in self]
        )
