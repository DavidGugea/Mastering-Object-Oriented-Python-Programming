import functools
from typing import Callable, Any, TypeVar, cast

FunctionDecoratorType = Callable[..., Any]
F = TypeVar("F", bound=FunctionDecoratorType)


def decorator_with_parameters(*decorator_args):
    def decorator(wrapped_function: F) -> F:
        @functools.wraps(wrapped_function)
        def wrapper(*args, **kwargs):
            print("Inside the wrapper [ before function execution ]")
            wrapped_function(*args, **kwargs)
            print("Inside the wrapper [ after function execution ]")
            print("Decorator args -- > {0}".format(decorator_args))

        return cast(F, wrapper)

    return decorator


def simple_decorator(wrapped_function: F) -> F:
    @functools.wraps(wrapped_function)
    def wrapper(*args, **kwargs):
        print("Inside the wrapper [ before function execution ]")
        wrapped_function(*args, **kwargs)
        print("Inside the wrapper [ after function execution ]")

    return cast(F, wrapper)


@decorator_with_parameters(1, 2, 3)
def test_function(number: int) -> None:
    print("Number given to test_function -- > {0}".format(number))


if __name__ == "__main__":
    """
    @simple_decorator 
    def test_function():
        ...
        
    = > test_function = simple_decorator(test_function)
    
    @decorator_with_parameters(*args)
    def test_function():
        ...
    = > test_function = decorator_with_parameters(args)(test_function)
    ||
    = > decorator = decorator_with_parameters(args)
    = > test_function = decorator(test_function)
    """
    test_function(5)
