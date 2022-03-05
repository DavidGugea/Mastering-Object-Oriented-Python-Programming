import argparse
from typing import Dict, Any


class Command:
    def __init__(self) -> None:
        self.config: Dict[str, Any] = {}

    def configure(self, namespace: argparse.Namespace) -> None:
        self.config.update(vars(namespace))

    def run(self) -> None:
        """Overridden by a subclass"""
        pass
