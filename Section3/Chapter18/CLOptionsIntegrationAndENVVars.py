import argparse
import sys
import os

parser = argparse.ArgumentParser

# Explicitly setting the values when defining the command-line options
parser.add_argument(
    "--samples",
    action="store",
    default=int(os.environ.get("SIM_SAMPLES", 100)),
    type=int,
    help="Samples to generate"
)

# Implicitly setting the values as part of the parsing process
config4 = argparse.Namespace()
config4.samples = int(os.environ.get("SIM_SAMPLES", 100))
config4a = parser.parse_args(sys.argv[1:], namespace=config4)
