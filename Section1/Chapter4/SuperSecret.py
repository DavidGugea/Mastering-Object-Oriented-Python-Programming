from typing import Any


class SuperSecret:
    def __init__(self, hidden: Any, exposed: Any) -> None:
        self._hidden = hidden
        self.exposed = exposed

    def __getattribute__(self, item: str):
        if (len(item) >= 2 and item[0] == "_") and item[1] != "_":
            raise AttributeError(item)

        return super().__getattribute__(item)


if __name__ == '__main__':
    x = SuperSecret("onething", "another")
    print(x.exposed)
    print(x._hidden)
