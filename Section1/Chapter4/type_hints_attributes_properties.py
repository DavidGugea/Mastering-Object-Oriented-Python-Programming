from typing import Optional


class RTD_Solver:
    def __init__(
            self,
            *,
            rate: Optional[float] = None,
            time: Optional[float] = None,
            distance: Optional[float] = None
    ) -> None:
        if rate:
            self.rate = rate
        if time:
            self.time = time
        if distance:
            self.distance = distance
