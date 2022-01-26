import argparse
import json
from pathlib import Path
import os
import sys
from collections import ChainMap
from typing import Dict, Any, List


def get_options(argv: List[str] = sys.argv[1:]) -> ChainMap:
    parser = argparse.ArgumentParser(
        description="Process some integers."
    )
    parser.add_argument(
        "-c", "--configuration", type=open, nargs="?"
    )
    parser.add_argument(
        "-p", "--playerclass", type=str, nargs="?",
        default="Simple"
    )
    cmdline = parser.parse_args(argv)

    if cmdline.configuration:
        config_file = json.load(cmdline.configuration)
        cmdline.configuration.close()
    else:
        config_file = {}

    default_path = (
            Path.cwd() / "Chpater_7" / "ch07_defaults.json"
    )

    with default_path.open() as default_file:
        defaults = json.load(default_file)

    combined = ChainMap(
        vars(cmdline), config_file, os.environ, defaults
    )

    return combined
