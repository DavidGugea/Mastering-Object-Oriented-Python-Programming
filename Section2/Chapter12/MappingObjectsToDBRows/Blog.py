from dataclasses import dataclass, field
from typing import List, Optional, cast, Any, Dict

from weakref import ref
from Post import Post

@dataclass
class Blog:
    title: str
    underline: str = field(init=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)
    _access: Optional[ref] = field(init=False, repr=False, default=None, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)

    @property
    def entries(self) -> List['Post']:
        if self._access and self._access():
            posts = cast('Access', self._access()).post_iter(self)
            return list(posts)

        raise RuntimeError("Can't work with Blog: no associated Access instance")

    def by_tag(self) -> Dict[str, List[Dict[str, Any]]]:
        if self._access and self._access():
            return cast('Access,', self._access()).post_by_tag(self)

        raise RuntimeError("Can't work with Blog: no associated Access instance")