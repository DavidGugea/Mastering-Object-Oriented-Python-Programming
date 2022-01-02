from dataclasses import dataclass, field


@dataclass(order=True)
class Investor:
    sort_index: float = field(init=False, repr=False)
    name: str
    age: int
    cash: float = field(repr=True, compare=False, default=0.0)

    def __post_init__(self):
        self.sort_index = self.cash


i1 = Investor("John", 80)
i2 = Investor("Mike", 18, 200)
i3 = Investor("John", 80, 600)

print(i1)
print(i1 > i3)