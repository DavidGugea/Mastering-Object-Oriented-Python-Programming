import logging
from typing import Any, Type


class UglyClass1:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


class UglyClass2:
    logger = logging.getLogger("UglyClass2")

    def __init__(self) -> None:
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


def logged(class_: Type) -> Type:
    class_.logger = logging.getLogger(class_.__qualname__)
    return class_


@logged
class SomeClass:
    def __init__(self) -> None:
        self.logger.info("New thing")  # mypy error

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


class LoggedWithHook:
    def __init_subclass__(cls, name=None):
        cls.logger = logging.getLogger(name or cls.__qualname__)


class SomeClass4(LoggedWithHook):
    def __init__(self) -> None:
        self.logger.info("New thing")  # mypy error

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42
