import argparse
import logging

__version__ = "3.8.10"

parser = argparse.ArgumentParser("Parser Test")

# on-off options
parser.add_argument('-v', '--verbose', action='store_true', default=False)
parser.add_argument(
    '--debug', action='store_const', const=logging.DEBUG,
    default=logging.INFO, dest='logging_level'
)

# option with an argument
parser.add_argument(
    "-b", "--bet", action="store", default="Flat",
    choices=["Flat", "Martingale", "OneThreeTwoSix"],
    dest="betting_rule"
)
parser.add_argument(
    "-s", "--stake", action="store", default=50, type=int
)

# positional arguments
parser.add_argument("input_filename", action="store")
parser.add_argument("output_filename", action="store")

# all other arguments

parser.add_argument(
    "filenames", action="store", nargs='*', metavar="file..."
)

# --version
parser.add_argument(
    "-V", "--version", action="version", version=__version__
)

config = parser.parse_args()


def process(filename: str):
    pass


for filename in config.filenames:
    process(filename)
