from collections import Counter
from LoggedClass import LoggedClass


class Main(LoggedClass):
    def __init__(self) -> None:
        self.counts: Counter[str] = Counter()

    def run(self) -> None:
        self.logger.info("Start")

        # Some processing in and around the counter increments
        self.counts["input"] += 2000
        self.counts["reject"] += 500
        self.counts["output"] += 1500

        self.logger.info(f"Counts {self.counts!s}")