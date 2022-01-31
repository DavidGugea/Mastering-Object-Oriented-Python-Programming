from typing import Any


class TestClass1:
    def __init__(self, value: int) -> None:
        self.value = value

    def __add__(self, other: int) -> None:
        print("[TestClass] Adding with -- > {0}".format(other))

    def __radd__(self, other: Any) -> None:
        print("[TestClass] radd with -- > {0}".format(other))


class TestClass2:
    def __init__(self, value: int) -> None:
        self.value = value

    def __add__(self, other: int) -> None:
        print("[TestClass2] Adding with -- > {0}".format(other))

    def __radd__(self, other: Any) -> None:
        print("[TestClass2] radd with -- > {0}".format(other))


if __name__ == '__main__':
    test1 = TestClass1(5)
    test2 = TestClass2(2)

    print(test1 + test2)
    print(test2 + test1)
