from typing import NamedTuple

class Person(NamedTuple):
    name: str
    age: int

test_person = Person("test_person_name", 23)
print(test_person.name)
print(test_person.age)
test_person.dynamic_instance_variable = 22