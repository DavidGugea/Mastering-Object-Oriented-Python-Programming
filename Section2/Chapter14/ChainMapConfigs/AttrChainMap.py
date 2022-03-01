from collections import ChainMap
from typing import Any


class AttrChainMap(ChainMap):
    def __getattr__(self, name: str) -> Any:
        if name == "maps":
            return self.__dict__["maps"]

        return super().get(name, None)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "maps":
            self.__dict__["maps"] = value
            return

        self[name] = value
