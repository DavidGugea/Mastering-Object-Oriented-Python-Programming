from dataclasses import dataclass


@dataclass
class Person:
    name: str 
    age: int

    def __post_init__(self):
        print(self.name)
        print(self.age)


test_person = Person("test_person_name", 23)
print(repr(test_person))
