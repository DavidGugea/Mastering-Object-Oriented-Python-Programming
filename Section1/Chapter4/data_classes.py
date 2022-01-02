from dataclasses import dataclass
from typing import Optional, cast


@dataclass
class RTD:
    rate: Optional[float]
    time: Optional[float]
    distance: Optional[float]

    def compute(self) -> "RTD":
        if(
            self.distance is None and self.rate is not None
            and self.time is not None
        ):
            self.distance = self.rate * self.time
        elif(
            self.rate is None and self.distance is not None
            and self.time is not None
        ):
            self.rate = self.distance / self.time
        elif (
            self.time is None and self.distance is not None
            and self.rate is not None
        ):
            self.time = self.distance / self.rate

        return self


