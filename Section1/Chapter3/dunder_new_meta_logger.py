import logging
from typing import cast, Type, Tuple, Dict, Any


class LoggedMeta(type):
    def __new__(
            cls: Type,
            name: str,
            bases: Tuple[Type, ...],
            namespace: Dict[str, Any]
    ):
        result = cast(
            "Logged", super().__new__(cls, name, bases, namespace)
        )

        result.logger = logging.getLogger(name)
        return result


class Logged(metaclass=LoggedMeta):
    logger: logging.Logger


class SomeApplicationClass(Logged):
    def __init__(self, v1: int, v2: int) -> None:
        self.logger.info("v1=%r, v2=%r", v1, v2)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v1 * v2
        self.logger.info("product=%r", self.v3)


