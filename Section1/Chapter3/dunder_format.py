from typing import Tuple


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (suit = {self.suit!r}, rank = {self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __format__(self, format_spec: str) -> str:
        """
        print(format_spec)

        if format_spec == "rank":
            return str(self.rank)
        elif format_spec == "suit":
            return str(self.suit)
        elif format_spec == "rank&suit":
            return "{0} {1}".format(self.rank, self.suit)
        else:
            return str(self)
        """

        if format_spec == "":
            return str(self)

        rs = (
            format_spec.replace("%r", str(self.rank))
                       .replace("%s", self.suit)
        )

        return rs


if __name__ == '__main__':
    card = Card(2, "♠")
    print(
        "{0:%r of %s}".format(card)
    )
