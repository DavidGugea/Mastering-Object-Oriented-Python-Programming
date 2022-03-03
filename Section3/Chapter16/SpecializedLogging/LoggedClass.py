import logging


class LoggedClassMeta(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        result = type.__new__(cls, name, bases, dict(namespace))
        result.logger = logging.getLogger(result.__qualname__)

        return result


class LoggedClass(metaclass=LoggedClassMeta):
    logger: logging.Logger
