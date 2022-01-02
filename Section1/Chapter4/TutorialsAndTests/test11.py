class Investor:
    def __init__(self, name: str, age: int, cash: float) -> None:
        self.name = name
        self.age = age
        self.cash = cash

    def __repr__(self) -> str:
        return "Name : {0}".format(self.name)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __lt__(self, other) -> bool:
        return self.cash < other.cash


i1 = Investor("John", 25, 9000)
i2 = Investor("Anna", 30, 12000)
i3 = Investor("Bob", 70, 800000)
i4 = Investor("John", 50, 100)

print(i1 == i4)
print(i1 > i4)
