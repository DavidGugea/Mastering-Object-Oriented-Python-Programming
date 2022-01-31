from typing import Any


class TestClass:
    def __init__(self, value: int) -> None:
        self.value = value

    def __add__(self, other: int) -> None:
        print("Adding with -- > {0}".format(other))

    def __radd__(self, other: Any) -> None:
        print("Radding with -- > {0}".format(other))


if __name__ == '__main__':
    test = TestClass(5)

    print(test + 2.15)
    print(2 + 2.15)
