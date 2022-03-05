import argparse 
import yaml
import logging
import logging.config
from typing import List 


class Setup_Logging:
    def __enter__(self, filename="logging.config") -> "Setup_Logging":
        logging.config.dictConfig(yaml.load(filename))

    def __exit__(self, *exc) -> None:
        logging.shutdown()

class Build_Config:
    def __init__(self, argv: List[str]) -> None:
        self.options = get_options_2(argv)

    def __enter__(self) -> argparse.Namespace:
        return self.options

    def __exit__(self, *exc) -> None:
        return


if __name__ == '__main__':
    with Setup_Logging():
        with Build_Config(arguments) as config_3:
            simulate_blackjack_betting(config_3)