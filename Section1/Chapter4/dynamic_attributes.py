class RTD_Solver:
    def __init__(
            self, *,
            rate: float = None,
            time: float = None,
            distance: float = None
    ):
        if rate:
            self.rate = rate
        if time:
            self.time = time
        if distance:
            self.distance = distance

    def __getattr__(self, item: str) -> float:
        if item == "rate":
            return self.distance / self.tiem
        elif item == "time":
            return self.distance / self.rate
        elif item == "distance":
            return self.rate * self.time
        else:
            raise AttributeError(f"Can't compute {item}")


if __name__ == '__main__':
    r1 = RTD_Solver(rate=6.25, distance=10.25)
    print(r1.time)
    print(r1.rate)
