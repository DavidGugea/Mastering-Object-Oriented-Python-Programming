import logging

logging.basicConfig(level=logging.INFO)


class LoggedAgeAccess:
    def __get__(self, obj, objtype):
        value = obj.age
        logging.info("Accessing %r giving %r", 'age', value)
        return value

    def __set__(self, obj, value) -> None:
        logging.info("Updating %r to %r", "age", value)
        obj._age = value


class Person:
    age = LoggedAgeAccess()  # Descriptor instance

    def __init__(self, name: str, age: int) -> None:
        self.name = name  # Regular instance attribute
        self.age = age  # Calls __set__()

    def birthday(self) -> None:
        self.age += 1  # Calls both __get__() and __set__() [ self.age = self.age + 1 ]


if __name__ == '__main__':
    test_person = Person("test_name", 23)
    print(vars(test_person))
