from typing import Type, Any


def memento(class_: Type) -> Type:
    def memento_method(self):
        return f"{self.__class__.__qualname__}(**{vars(self)!r})"

    class_.memento = memento_method
    return class_


@memento
class StatefulClass:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"


class Memento:
    def memento(self) -> str:
        return f"{self.__class__.__qualname__}" f"(**{vars(self)!r})"


class StatefulClass2(Memento):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


if __name__ == "__main__":
    st = StatefulClass(2.7)
    print(st.memento())
