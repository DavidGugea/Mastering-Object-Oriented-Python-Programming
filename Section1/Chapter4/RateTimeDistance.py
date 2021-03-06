from typing import Optional
from dataclasses import dataclass

"""
The generated __init__() code will call a method named __post_init__(), if __post_init__() is defined on the class. 
It will normally be called as self.__post_init__(). 

The __init__() method generated by dataclass() does not call base class __init__() methods. 
If the base class has an __init__() method that has to be called, it is common to call this method in a __post_init__() 
method.
"""


@dataclass()
class RateTimeDistance:
    rate: Optional[float] = None
    time: Optional[float] = None
    distance: Optional[float] = None

    def __post_init__(self) -> None:
        print("POST INIT")
        if self.rate is not None and self.time is not None:
            self.distance = self.rate * self.time
        elif self.rate is not None and self.distance is not None:
            self.time = self.distance / self.rate
        elif self.time is not None and self.distance is not None:
            self.rate = self.distance / self.time


if __name__ == '__main__':
    r1 = RateTimeDistance(time=1, rate=0)
    print(r1.distance)
