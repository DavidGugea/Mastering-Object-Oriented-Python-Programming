import collections.abc
from typing import Callable, Dict

IntExp = Callable[[int, int], int]


class Power1:
    def __init__(self, a: str):
        self.a = a

    def __call__(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x

        return p


class Power2(collections.abc.Callable):
    def __call__(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x

        return p


class Power3:
    def __call_(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x

        return p


class Power4:
    def __call__(self, x: int, n: int) -> int:
        if n == 0:
            return 1
        elif n % 2 == 1:
            return self.__call__(x, n - 1) * x
        else:
            t = self.__call__(x, n // 2)
            return t * t


class Power5:
    def __init__(self) -> None:
        self.memo: Dict = {}

    def __call__(self, x: int, n: int) -> int:
        if (x, n) not in self.memo:
            if n == 0:
                self.memo[x, n] = 1
            elif n % 2 == 1:
                self.memo[x, n] = self.__call__(x, n - 1) * x
            elif n % 2 == 0:
                self.memo[x, n] = self.__call__(x, n // 2)
            else:
                raise Exception("Logic Error")

        return self.memo[x, n]


if __name__ == "__main__":
    pow5: IntExp = Power4()
    print(pow5(2, 1024))
    print(pow5(2, 1024))
