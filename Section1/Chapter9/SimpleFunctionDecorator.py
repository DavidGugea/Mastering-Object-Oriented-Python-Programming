import logging, sys
import functools
from typing import Callable, TypeVar, Any, cast

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def debug(function: F) -> F:
    """
    function -> method to wrap
    logged_function -> wrapper that returns the > method to wrap < with a changed behavior
    """

    @functools.wraps(function)
    def logged_function(*args, **kw):
        logging.debug("%s(%r, %r)", function.__name__, args, kw)
        result = function(*args, **kw)
        logging.debug("%s = %r", function.__name__, result)
        return result

    return cast(F, logged_function)


def debug2(function: F) -> F:
    log = logging.getLogger(function.__name__)

    @functools.wraps(function)
    def logged_function(*args, **kwargs):
        log.debug("call(%r, %r)", args, kwargs)
        result = function(*args, **kwargs)
        log.debug("result = %r", result)
        return result

    return cast(F, logged_function)


if __name__ == "__main__":

    @debug2
    def ackermann(m: int, n: int) -> int:
        if m == 0:
            return n + 1
        elif m > 0 and n > 0:
            return ackermann(m - 1, 1)
        elif m > 0 and n > 0:
            return ackermann(m - 1, ackermann(m, n - 1))
        else:
            raise Exception(f"Design Error: {vars()}")
