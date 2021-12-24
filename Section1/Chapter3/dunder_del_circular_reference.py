from typing import cast


class Parent:
    def __init__(self, *children: "Child") -> None:
        for child in children:
            child.parent = self

        self.children = {c.id: c for c in children}

    def __del__(self) -> None:
        print(
            f"Removing {self.__class__.__name__} {id(self):d}"
        )


class Child:
    def __init__(self, id: str) -> None:
        self.id = id
        self.parent: Parent = cast(Parent, None)

    def __del__(self) -> None:
        print(
            f"Removing {self.__class__.__name__} {id(self):d}"
        )
