class Circle:
    pi: int = 3.14

    def __init__(self, radius: int) -> None:
        self.radius = radius

    def __setattr__(self, key: str, value) -> None:
        if key == "pi":
            raise ValueError("Can't change the value of >>pi<<. It is a read-only class variable.")
        else:
            super().__setattr__(key, value)


if __name__ == '__main__':
    c = Circle(5)
    print(c.radius)
    print(c.pi)
