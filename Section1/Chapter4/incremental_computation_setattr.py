class RTD_Dynamic:
    def __init__(self) -> None:
        self.rate: float
        self.time: float
        self.distance: float

        super().__setattr__('rate', None)
        super().__setattr__('time', None)
        super().__setattr__('distance', None)

    def __repr__(self) -> str:
        clauses = []
        if self.rate:
            clauses.append(f"rate={self.rate}")
        if self.time:
            clauses.append(f"time=${self.time}")
        if self.distance:
            clauses.append(f"distance=${self.distance}")
        return (
            f"{self.__class__.__name__}"
            f"({', '.join(clauses)}"
        )

    def __setattr__(self, name: str, value: float) -> None:
        if name == "rate":
            super().__setattr__('rate', value)
        elif name == "time":
            super().__setattr__("time", value)
        elif name == "distance":
            super().__setattr__("distance", value)

        if self.rate and self.time:
            super().__setattr__("distance", self.rate * self.time)
        elif self.rate and self.distance:
            super().__setattr__("time", self.distance / self.rate)
        elif self.time and self.distance:
            super().__setattr__("rate", self.distance / self.time)