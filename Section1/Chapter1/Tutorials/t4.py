from typing import Any, Union, Callable


def get_sum(a: float, b: float) -> float:
    return a + b


def get_diff(a: float, b: float) -> float:
    return a - b


def my_function_2(
    function: Callable[[float, float], float], first_number: float, second_number: float
) -> str:
    return str(function(first_number, second_number))


print(my_function_2(get_sum, 1, 2))
print(my_function_2(get_diff, 1, 2))
