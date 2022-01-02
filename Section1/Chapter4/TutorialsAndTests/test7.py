import logging

logging.basicConfig(level=logging.INFO)


class LoggedAccess:
    def __set_name__(self, owner, name):
        print("DUNDER SET NAME CALLED. Owner : {0} || Name : {1}".format(
            owner, name
        ))
        self.public_name = name
        self.private_name = "_{0}".format(name)
        print("public_name : {0} && private_name : {1}".format(
            self.public_name,
            self.private_name
        ))

    def __get__(self, obj, objtype):
        value = getattr(obj, self.private_name)
        logging.info("Accessing {0} giving {1}".format(
            self.public_name,
            value
        ))
        return value

    def __set__(self, obj, value) -> None:
        logging.info("Updating {0} to {1}".format(
            self.public_name,
            value
        ))
        setattr(obj, self.private_name, value)


class Person:
    name = LoggedAccess()  # First descriptor instance
    age = LoggedAccess()  # Second descriptor instance

    def __init__(self, name: str, age: int) -> None:
        self.name = name  # Calls the first descriptor
        self.age = age  # Calls the second descriptor

    def birthday(self) -> None:
        self.age += 1


if __name__ == '__main__':
    test_person = Person("test_name", 23)
    print(test_person.age)
    test_person.age = 15
    test_person.name = "test_name_2"
