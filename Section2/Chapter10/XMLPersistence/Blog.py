from typing import List, Dict, Any, DefaultDict
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from Post import Post


@dataclass
class Blog:
    title: str
    entries: List[Post] = field(default_factory=list)
    underline: str = field(init=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)

    def append(self, post: Post) -> None:
        self.entries.append(post)

    def by_tag(self) -> DefaultDict[str, List[Dict[str, Any]]]:
        tag_index: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in self.entries:
            for tag in post.tags:
                tag_index[tag].append(asdict(post))

        return tag_index

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def xml(self) -> str:
        children = "\n".join(c.xml() for c in self.entries)
        return f"""\
<blog><title>{self.title}</title>
<entries>
{children}
</entries>
</blog>"""
