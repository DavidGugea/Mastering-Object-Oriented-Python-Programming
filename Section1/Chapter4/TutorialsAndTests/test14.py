import logging

logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
logging_formatter = logging.Formatter(
    fmt="{levelname} -- > {message}",
    style="{"
)
stream_handler.setFormatter(logging_formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class LoggingDescriptor:
    def __init__(self, value, name) -> None:
        self.value = value
        self.name = name

    def __get__(self, obj, objtype):
        logger.info("Retrieving property {0} with the value {1} from the object {2} [ Type : {3} ]".format(
            self.name,
            self.value,
            obj,
            objtype
        ))

        return self.value

    def __set__(self, instance, new_value) -> None:
        logger.info("Setting the property {0} to the value {1} from the object {2}".format(
            self.name,
            new_value,
            instance,
        ))

        self.value = new_value


class Person:
    age: [int | LoggingDescriptor] = LoggingDescriptor(None, "age")
    name: [str | LoggingDescriptor] = LoggingDescriptor(None, "name")

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


if __name__ == '__main__':
    test_person = Person("test_person_name", 23)
    print(test_person.name)
    print(test_person.age)
