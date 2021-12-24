from typing import Any


class TestClass:
    def __init__(self, x: Any, y: Any) -> None:
        self.x = x
        self.y = y

    def __format__(self, format_spec: str) -> str:
        print("format_spec -- > {0}".format(format_spec))

        return str(self)


if __name__ == '__main__':
    test_class = TestClass(1, 2)
    width = 6
    print(
        f"{test_class:{width}}"
    )