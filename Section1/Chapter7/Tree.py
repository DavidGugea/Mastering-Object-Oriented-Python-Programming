import collections.abc
import weakref
from abc import ABCMeta, abstractmethod
from typing import Iterable, Any, cast, Iterator, Optional


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...

    @abstractmethod
    def __ge__(self, other: Any) -> bool: ...


class TreeNode:
    def __init__(
            self,
            item: Optional[Comparable] = None,
            less: Optional["TreeNode"] = None,
            more: Optional["TreeNode"] = None,
            parent: Optional["TreeNode"] = None,
    ) -> None:
        self.item = item
        self.less = less
        self.more = more
        if self.parent:
            self.parent = parent

    @property
    def parent(self) -> Optional["TreeNode"]:
        return self.parent_ref()

    @parent.setter
    def parent(self, value: "TreeNode"):
        self.parent_ref = weakref.ref(value)

    def __repr__(self) -> str:
        return f"TreeNode ({self.item!r}, {self.less!r}, {self.more!r})"

    def find(self, item: Comparable) -> "TreeNode":
        if self.item is None:
            if self.more:
                return self.more.find(item)
        elif self.item == item:
            return self
        elif self.item > item and self.less:
            return self.less.find(item)
        elif self.item < item and self.more:
            return self.more.find(item)
        raise KeyError

    def __iter__(self) -> Iterator[Comparable]:
        if self.less:
            yield from self.less
        if self.item:
            yield from self.item
        if self.more:
            yield from self.more

    def add(self, item: Comparable) -> None:
        if self.item is None:
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)
        elif self.item >= item:
            if self.less:
                self.less.add(item)
            else:
                self.less = TreeNode(item, parent=self)
        elif self.item < item:
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)

    def remove(self, item: Comparable) -> None:
        if self.item is None or item > self.item:
            if self.more:
                self.more.remove(item)
            else:
                raise KeyError
        elif item < self.item:
            if self.less:
                self.less.remove(item)
            else:
                raise KeyError
        else:
            if self.less and self.more:
                successor = self.more._least()
                self.item = successor.item
                if successor.item:
                    successor.remove(successor.item)
                elif self.less:
                    self._replace(self.less)
                elif self.more:
                    self._replace(self.more)
                else:
                    self._replace(None)

    def _least(self) -> "TreeNode":
        if self.less is None:
            return self

        return self.less._least()

    def _replace(self, new: Optional["TreeNode"] = None) -> None:
        if self.parent:
            if self == self.parent.less:
                self.parent.less = new
            else:
                self.parent.more = new
        if new is not None:
            new.parent = self.parent


class Tree(collections.abc.MutableSet):
    def __init__(self, source: Iterable[Comparable] = None) -> None:
        self.root = TreeNode(None)
        self.size = 0
        if source:
            for item in source:
                self.root.add(item)
                self.size += 1

    def add(self, item: Comparable) -> None:
        self.root.add(item)
        self.size += 1

    def discard(self, item: Comparable) -> None:
        if self.root.more:
            try:
                self.root.more.remove(item)
                self.size -= 1
            except KeyError:
                pass
        else:
            pass

    def __contains__(self, item: Any) -> bool:
        if self.root.more:
            self.root.more.find(cast(Comparable, item))
            return True
        else:
            return False

    def __iter__(self) -> Iterator[Comparable]:
        if self.root.more:
            for item in iter(self.root.more):
                yield item

    def __len__(self) -> int:
        return self.size
