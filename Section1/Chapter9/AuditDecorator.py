import logging, sys
import functools
from enum import Enum
from typing import Callable, TypeVar, Any, cast

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


class Suit(Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


class CardDC:
    def __init__(self, rank: int, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit


def audit(method: F) -> F:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        template = "%s\n    before %s\n     after %s"
        audit_log = logging.getLogger("audit")
        before = repr(self)

        try:
            result = method(self, *args, **kwargs)
        except Exception as e:
            after = repr(self)
            audit_log.exception(template, method.__qualname__, before, after)
            raise

        after = repr(self)
        audit_log.info(template, method.__qualname__, before, after)

        return result

    return cast(F, wrapper)


class Hand:
    def __init__(self, *cards: CardDC) -> None:
        self._cards = list(cards)

    @audit
    def __iadd__(self, card: CardDC) -> "Hand":
        self._cards.append(card)
        self._cards.sort(key=lambda c: c.rank)
        return self

    def __repr__(self) -> str:
        cards = ", ".join(map(str, self._cards))
        return f"{self.__class__.__name__}({cards})"
