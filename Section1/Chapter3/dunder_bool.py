from typing import Any


class Container:
    def __init__(self, *items: Any) -> None:
        self.items: list = list(items)

    def add(self, *items: Any):
        for item in items:
            self.items.append(item)

    def delete(self, item: Any):
        self.items.remove(item)

    def __bool__(self) -> bool:
        return bool(self.items)

    def __str__(self) -> str:
        return ", ".join(map(str, self.items))


class ListContainer(list):
    def __init__(self, *items: Any) -> None:
        super().__init__(items)


if __name__ == '__main__':
    list_container = ListContainer()
    print(bool(list_container))
    print(list_container)
    list_container.extend([1, 2, 3])
    print(bool(list_container))
    print(list_container)

    container = Container()
    print(bool(container))

    container.add(1, 2, 3)
    print(container)
    container.add(4, 5)
    print(container)

    print(bool(container))
