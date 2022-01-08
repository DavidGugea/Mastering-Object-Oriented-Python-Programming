from typing import Tuple, Iterator, Any


class LikeAbstract:
    def aMethod(self, arg: int) -> int:
        raise NotImplementedError


class LikeConcrete(LikeAbstract):
    def aMethod(self, arg1: str, arg2: Tuple[int, int]) -> Iterator[Any]:
        pass