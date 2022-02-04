from typing import Type, List
from enum import Enum


class Suits(str, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


class EnumDomain:
    @classmethod
    def domain(cls: Type) -> List[str]:
        return [m.value for m in cls]


class SuitD(str, EnumDomain, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"
