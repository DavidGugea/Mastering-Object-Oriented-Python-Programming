import logging
from AudietClassMeta import AuditedClassMeta
from LoggedClass import LoggedClass


class AuditedClass(LoggedClass, metaclass=AuditedClassMeta):
    audit: logging.Logger
    pass