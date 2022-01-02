from dataclasses import dataclass, field


@dataclass
class Person:
    first_name: str = field()
    last_name: str = field()
    age: int = field()
    full_name: str = field(repr=False, init=False)

    def __post_init__(self) -> None:
        self.full_name = "{0} {1}".format(self.first_name, self.last_name)


if __name__ == '__main__':
    test_person = Person("test_first_name", "test_last_name", 15)
    print(test_person)
    print("Full name is -- > {0}".format(test_person.full_name))
