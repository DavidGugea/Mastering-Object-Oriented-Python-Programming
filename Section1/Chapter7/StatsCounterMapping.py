import math
from collections import Counter


class StatsCounter(Counter):
    @property
    def mean(self) -> float:
        sum0 = sum(v for k, v in self.items())
        sum1 = sum(k * v for k, v in self.items())
        return sum1 / sum0

    @property
    def stdev(self) -> float:
        sum0 = sum(v for k, v in self.items())
        sum1 = sum(k * v for k, v in self.items())
        sum2 = sum(k * k * v for k, v in self.items())
        return math.sqrt(
            sum0 * sum2 - sum1 * sum1
        ) / sum0
