__all__ = ["TestClass1", "TestClass2"]


class TestClass1:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def add(self) -> int:
        return self.a + self.b


class TestClass2:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def multiply(self) -> int:
        return self.a * self.b


class TestClass3:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def divide(self) -> float:
        return self.a / self.b


def func():
    print("test")