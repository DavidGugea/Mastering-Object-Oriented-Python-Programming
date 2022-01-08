import collections.abc
from collections.abc import Iterator


class SomeApplication(collections.abc.Sequence):
    def some_method(self, other: Iterator):
        assert isinstance(other, collections.abc.Iterator)
