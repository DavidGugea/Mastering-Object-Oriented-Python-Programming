from typing import Any, Callable, TypeVar, cast

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def my_decorator(func: F) -> F:
    ...
