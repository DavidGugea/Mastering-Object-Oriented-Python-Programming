import logging, sys
import functools
from typing import Callable, TypeVar, Any, cast

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def debug_named(log_name: str) -> Callable[[F], F]:
    log = logging.getLogger(log_name)

    def concrete_decorator(function: F) -> F:
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            log.debug("%s(%r, %r)", function.__name__, args, kwargs)
            result = function(args, kwargs)
            log.debug("%s = %r", function.__name__, result)

            return result

        return cast(F, wrapped)

    return concrete_decorator


if __name__ == "__main__":

    @debug_named("recursion")
    def ackermann3(m: int, n: int) -> int:
        if m == 0:
            return n + 1
        elif m > 0 and n > 0:
            return ackermann3(m - 1, 1)
        elif m > 0 and n > 0:
            return ackermann3(m - 1, ackermann3(m, n - 1))
        else:
            raise Exception(f"Design Error: {vars()}")
