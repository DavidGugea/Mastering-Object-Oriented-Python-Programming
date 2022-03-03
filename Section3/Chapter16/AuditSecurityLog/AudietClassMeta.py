import logging
from LoggedClass import LoggedClassMeta


class AuditedClassMeta(LoggedClassMeta):
    def __new__(cls, name, bases, namespace, **kwargs):
        result = LoggedClassMeta.__new__(cls, name, bases, dict(namespace))
        for item, type_ref in result.__annotations__.items():
            if issubclass(type_ref, logging.Logger):
                prefix = "" if item == "logger" else f"{item}."
                logger = logging.getLogger(f"{prefix}{result.__qualname__}")
                setattr(result, item, logger)

            return result