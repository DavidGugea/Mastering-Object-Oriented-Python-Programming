from typing import Any


class Test:
    def __init__(self, value: int, second_value: Any) -> None:
        self._value = value
        self.second_value = second_value

    @property
    def value(self) -> int:
        print("Accessed the getter")
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        print("Accessed the setter")
        if 0 < new_value < 100:
            self._value = new_value
        else:
            raise ValueError("The value must be between 0 and 100")

    @value.deleter
    def value(self) -> None:
        print("Accessed the deleter")
        raise Exception("You can't delete the value")

    def __getattr__(self, item: str) -> Any:
        print("< ------- Get attribute accessed for item : {0} ------- >".format(item))


if __name__ == '__main__':
    test = Test(5, 10)
    print(test.value)
    print(test.second_value)
    print(test.asdf)