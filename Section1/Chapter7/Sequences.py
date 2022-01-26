from typing import List, Optional, Iterable, cast, Any, overload, Union
import math


def mean(outcomes: List[float]) -> float:
    return sum(outcomes) / len(outcomes)


class StatsList(list):
    def __init__(self, iterable: Optional[Iterable[float]]) -> None:
        super().__init__(cast(Iterable[Any], iterable))

    @property
    def mean(self) -> float:
        return sum(self) / len(self)

    @property
    def stdev(self) -> float:
        n = len(self)
        return math.sqrt(
            n * sum(x ** 2 for x in self) - sum(self) ** 2
        ) / n


class StatsList2(list):
    """Eager Stats."""

    def __init__(self, iterable: Optional[Iterable[float]]) -> None:
        self.sum0 = 0
        self.sum1 = 0.0
        self.sum2 = 0.0
        super().__init__(cast(Iterable[Any], iterable))
        for x in self:
            self._new(x)

    def _new(self, value: float) -> None:
        self.sum0 += 1
        self.sum1 += value
        self.sum2 += value * value

    def _rmv(self, value: float) -> None:
        self.sum0 -= 1
        self.sum1 -= value
        self.sum2 -= value * value

    def insert(self, index: int, value: float) -> None:
        super().insert(index, value)
        self._new(value)

    def pop(self, index: int = 0) -> None:
        value = super().pop(index)
        self._rmv(value)
        return value

    @overload
    def __setitem__(self, index: int, value: float) -> None:
        pass

    @overload
    def __setitem__(self, index: int, value: Iterable[float]) -> None:
        pass

    def __setitem__(self, index, value) -> None:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            olds = [self[i] for i in range(start, stop, step)]
            super().__setitem__(index, value)

            for x in olds:
                self._rmv(x)
            for x in value:
                self._new(x)
        else:
            old = self[index]
            super().__setitem__(index, value)
            self._rmv(old)

    def __delitem(self, index: Union[int, slice]) -> None:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            olds = [self[i] for i in range(start, stop, step)]
            super().__setitem__(index)

            for x in olds:
                self._rmv(x)
        else:
            old = self[index]
            super().__setitem__(index)
            self._rmv(old)

    @property
    def mean(self) -> float:
        return self.sum1 / self.sum0

    @property
    def stdev(self) -> float:
        return math.sqrt(
            self.sum0 * self.sum2 - self.sum1 * self.sum1
        ) / self.sum0


class StatsList3:
    def __init__(self) -> None:
        self._list: List[float] = list()
        self.sum0 = 0
        self.sum1 = 0.0
        self.sum2 = 0.0

    def append(self, value: float) -> None:
        self._list.append(value)
        self.sum0 += 1
        self.sum1 += value
        self.sum2 += value * value

    def __getitem__(self, index: int) -> float:
        return self._list.__getitem__(index)

    @property
    def mean(self) -> float:
        return self.sum1 / self.sum0

    @property
    def stdev(self) -> float:
        return math.sqrt(
            self.sum0 * self.sum2 - self.sum1 * self.sum1
        ) / self.sum0


if __name__ == '__main__':
    s12 = StatsList2([2, 4, 3, 4, 5, 5, 7, 9, 10])
    print(
        s12.sum0,
        s12.sum1,
        s12.sum2
    )
    s12[2] = 4
    print(
        s12.sum0,
        s12.sum1,
        s12.sum2
    )
    del s12[-1]
    print(
        s12.sum0,
        s12.sum1,
        s12.sum2
    )
    s12.insert(0, -1)
    print(
        s12.sum0,
        s12.sum1,
        s12.sum2
    )
    s12.pop()
    print(
        s12.sum0,
        s12.sum1,
        s12.sum2
    )
