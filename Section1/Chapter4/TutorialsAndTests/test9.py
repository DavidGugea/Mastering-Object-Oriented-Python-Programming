import logging

logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
logger_stream_handler = logging.StreamHandler()
logger_formatter = logging.Formatter(
    fmt="{lineno} - {levelname} - {message}",
    style="{"
)
logger_stream_handler.setFormatter(logger_formatter)
logger.addHandler(logger_stream_handler)


class LoggerDataDescriptor:
    def __init__(self, value, property_name) -> None:
        self.value = value
        self.property_name = property_name

    def __set__(self, instance, value) -> None:
        logger.info("Setting the value of {0} to {1}".format(
            self.property_name,
            value
        ))

        self.value = value

    def __get__(self, instance, owner):
        logger.info(
            "Getting the value of {0}".format(self.property_name)
        )

        return self.value


class Person:
    name: [str | LoggerDataDescriptor] = LoggerDataDescriptor("", "name")
    age: [int | LoggerDataDescriptor] = LoggerDataDescriptor(0, "age")

    def __init__(self, name: str, age: int) -> None:
        self.name = name  # Accessing the setter from the name descriptor
        self.age = age  # Accessing the setter from the age descriptor


if __name__ == '__main__':
    test_person = Person("test_name", 23)
    print(test_person.name)
    print(test_person.age)

    test_person.name = "test_name_2"
    test_person.age = 20

    print(test_person.name)
    print(test_person.age)
