from hand import Suit


class BlackJackCard:
    __slots__ = ("rank", "suit", "hard", "soft")

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft
