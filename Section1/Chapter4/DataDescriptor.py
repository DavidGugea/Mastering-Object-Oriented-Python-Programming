from typing import Any, Type, Optional


class Conversion:
    """Depends on a standard value."""
    conversion: float
    standard: str

    def __get__(self, instance: Any, owner: Type) -> float:
        return getattr(instance, self.standard) * self.conversion

    def __set__(self, instance: Any, value: float) -> None:
        setattr(instance, self.standard, value / self.conversion)


class Standard(Conversion):
    """Define a standard value."""
    conversion = 1.0


class Speed(Conversion):
    standard = "standard_speed"  # KPH


class KPH(Standard, Speed):
    pass


class Knots(Speed):
    conversion = 0.5399568


class MPH(Speed):
    conversion = 0.62137119


class Trip:
    kph = KPH()
    knots = Knots()
    mph = MPH()

    def __init__(
            self,
            distance: float,
            kph: Optional[float] = None,
            mph: Optional[float] = None,
            knots: Optional[float] = None,
    ) -> None:
        self.distance = distance  # Nautical Miles
        if kph:
            self.kph = kph
        elif mph:
            self.mph = mph
        elif knots:
            self.knots = knots
        else:
            raise TypeError("Impossible Arguments")

        self.time = self.distance / self.knots

    def __str__(self) -> str:
        return (
            f"distance: {self.distance} nm,"
            f"kph: {self.kph}"
            f"mph: {self.mph}"
            f"knots: {self.knots} knots, "
            f"time: {self.time} hrs"
        )


if __name__ == '__main__':
    m2 = Trip(distance=13.2, knots=5.9)
    print(m2)
    print(f"Speed: {m2.mph:.3f} mph")
    print(m2.standard_speed)
