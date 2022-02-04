import math


class Angle(float):
    __slots__ = ("_degrees",)

    def __init__(self, degrees: float) -> None:
        self._degrees = degrees

    @staticmethod
    def from_radians(value: float) -> "Angle":
        return Angle(180 * value / math.pi)

    @property
    def radians(self) -> float:
        return math.pi * self._degrees / 180

    @property
    def degrees(self) -> float:
        return self._degrees
