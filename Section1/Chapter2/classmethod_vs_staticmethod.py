class TestClass:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    @staticmethod
    def test_static_method() -> None:
        print("You have use the static method")

    @classmethod
    def test_class_method(cls):
        print(repr(cls))


if __name__ == "__main__":
    x = TestClass(1, 2)
    x.test_static_method()
    x.test_class_method()
