class RTD_Dymamic:
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
