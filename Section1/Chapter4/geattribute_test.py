"""
A key difference between __getattr__ and __getattribute__ is that __getattr__ is only invoked if the attribute wasn't
found the usual ways. It's good for implementing a fallback for missing
attributes, and is probably the one of two you want.
__getattribute__ is invoked before looking at the actual attributes on the object, and so can be tricky to implement
correctly. You can end up in infinite recursions very easily.
New-style classes derive from object, old-style classes are those in Python 2.x with no explicit base class.
But the distinction between old-style and new-style classes is not the important one when choosing between __getattr__
and __getattribute__.
You almost certainly want __getattr__.

https://stackoverflow.com/questions/3278077/difference-between-getattr-vs-getattribute

Short answer:

__getattr__ is only called when the item is not known
__getattribute__ is always called
"""

from typing import Any


class TestClass:
    def __init__(self, value: int) -> None:
        self.value = value

    def __getattr__(self, item: Any) -> None:
        print("GETATTR ITEM -- > {0}".format(item))
        # getattr(self, item)

    def __getattribute__(self, item: Any) -> None:
        print("GETATTRIBUTE ITEM -- > {0}".format(item))
        super().__getattribute__(item)


if __name__ == '__main__':
    x = TestClass(5)
    print(x.value)
    print(x.a)