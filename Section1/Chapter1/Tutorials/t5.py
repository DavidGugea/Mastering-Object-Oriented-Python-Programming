from typing import *
import timeit

"""
input_list = range(100)


def div_by_five(num: int) -> bool:
    if num % 5 == 0:
        return True
    else:
        return False


xyz: Generator[int] = (i for i in input_list if div_by_five(i))
abc: List[int] = [i for i in input_list if div_by_five(i)]
"""

print(
    timeit.timeit(
        """
input_list = range(100)


def div_by_five(num: int) -> bool:
    if num % 5 == 0:
        return True
    else:
        return False


xyz: Any[int] = ([i for i in input_list if div_by_five(i)])
""",
        number=5000,
    )
)
