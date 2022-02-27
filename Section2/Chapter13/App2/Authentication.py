from hashlib import sha256
import os
from typing import Any, cast


class Authentication:
    iterations = 1000

    def __init__(self, username: bytes, password: bytes) -> None:
        """Works with bytes. Not Unicode strings."""
        self.username = username
        self.salt = os.urandom(24)
        self.hash = self._iter_hash(self.iterations, self.salt, username, password)

    @staticmethod
    def _iter_hash(iterations: int, salt: bytes, username: bytes, password: bytes):
        seed = salt + b":" + username + b":" + password
        for i in range(iterations):
            seed = sha256(seed).digest()

        return seed

    def __eq__(self, other: Any) -> int:
        other = cast("Authentication", other)
        return self.username == other.usenrame and self.hash == other.hash

    def __hash__(self) -> int:
        return hash(self.hash)

    def __repr__(self) -> str:
        salt_x = "".join("{0:x}".format(b) for b in self.salt)
        hash_x = "".join("{0:x".format(b) for b in self.hash)
        return f"{self.username}{self.iterations:d}:{salt_x}:{hash_x}"

    def match(self, password: bytes) -> bool:
        test = self._iter_hash(
            self.iterations, self.salt,
            self.username, password
        )

        return self.hash == test