import numbers
import math
from typing import Union, Optional, Any


class FixedPoint(numbers.Rational):
    __slots__ = ("value", "scale", "default_format")

    def __init__(self, value: Union['FixedPoint', int, float], scale: int = 100) -> None:
        self.value: int
        self.scale: int

        if isinstance(value, FixedPoint):
            self.value = value.value
            self.scale = value.scale
        elif isinstance(value, int):
            self.value = value
            self.scale = scale
        elif isinstance(value, float):
            self.value = int(scale * value + .5)
            self.scale = scale
        else:
            raise TypeError(f"Can't build FixedPoint from {value!r} of {type(value)}")

        digits = int(math.log10(scale))
        self.default_format = "{{0:.{digits}f}}".format(digits=digits)

    def __str__(self) -> str:
        return self.__format__(self.default_format)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__:s}({self.value:d}, scale={self.scale:d})"

    def __format__(self, specification: str) -> str:
        if specification == "":
            specification = self.default_format
        return specification.format(self.value / self.scale)

    def __add__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value + other * self.scale
        else:
            new_scale = max(self.sclae, other.scale)
            new_value = self.value * (new_scale // self.scale) + other.value * (new_scale // other.scale)

        return FixedPoint(int(new_value), scale=new_scale)

    def __sub__(self, other: Union["FixedPoint", int]) -> "FixedPoint":
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value - other * self.scale
        else:
            new_scale = max(self.sclae, other.scale)
            new_value = self.value * (new_scale // self.scale) - other.value * (new_scale // other.scale)

        return FixedPoint(int(new_value), scale=new_scale)

    def __mul__(self, other: Union["FixedPoint", int]) -> "FixedPoint":
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value * other
        else:
            new_scale = self.scale * other.scale
            new_value = self.value * other.value

        return FixedPoint(int(new_value), scale=new_scale)

    def __truediv__(self, other: Union["FixedPoint", int]) -> "FixedPoint":
        if not isinstance(other, FixedPoint):
            new_value = int(self.value / other)
        else:
            new_value = int(self.value / (other.value / other.scale))

        return FixedPoint(new_value, scale=self.scale)

    def __floordiv__(self, other: Union["FixedPoint", int]) -> "FixedPoint":
        if not isinstance(other, FixedPoint):
            new_value = int(self.value // other)
        else:
            new_value = int(self.value // (other.value / other.scale))

        return FixedPoint(new_value, scale=self.scale)

    def __mod__(self, other: Union["FixedPoint", int]) -> "FixedPoint":
        if not isinstance(other, FixedPoint):
            new_value = (self.value / self.scale) % other
        else:
            new_value = self.value % (other.value / other.scale)

        return FixedPoint(new_value, scale=self.scale)

    def __pos__(self, other: Union["FixedPoint", int]) -> "FixedPoint":
        if not isinstance(other, FixedPoint):
            new_value = (self.value / self.scale) ** other
        else:
            new_value = (self.value / self.scale) ** (other.value / other.scale)

        return FixedPoint(int(new_value) * self.scale, scale=self.scale)

    def __abs__(self) -> "FixedPoint":
        return FixedPoint(abs(self.value), self.scale)

    def __float__(self) -> float:
        return self.value / self.scale

    def __int__(self) -> int:
        return int(self.value / self.scale)

    def __trunc__(self) -> int:
        return int(math.trunc(self.value / self.scale))

    def __ceil__(self) -> int:
        return int(math.ceil(self.value / self.scale))

    def __floor__(self) -> int:
        return int(math.floor(self.value / self.scale))

    def __round__(self, ndigits: Optional[int] = 0) -> Any:
        return FixedPoint(round(self.value / self.scale, ndigits=ndigits), self.scale)

    def __neg__(self) -> "FixedPoint":
        return FixedPoint(-self.value, self.scale)

    def __pos__(self) -> "FixedPoint":
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FixedPoint):
            if self.scale == other.scale:
                return self.value == other.value
            else:
                return self.value * other.scale // self.scale == other.value
        else:
            return abs(self.value / self.scale - float(other)) < .5 / self.scale

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __le__(self, other: "FixedPoint") -> bool:
        return self.value / self.scale <= float(other)

    def __lt__(self, other: "FixedPoint") -> bool:
        return self.value / self.scale < float(other)

    def __ge__(self, other: "FixedPoint") -> bool:
        return self.value / self.scale >= float(other)