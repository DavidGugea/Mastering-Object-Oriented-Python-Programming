import yaml
import os
import argparse
from pathlib import Path
from collections import ChainMap
from typing import Optional


def nint(x: Optional[str]) -> Optional[int]:
    if x is None:
        return x

    return int(x)


config_locations = (
    Path.cwd(),
    Path.home(),
    Path.cwd() / "opt",
    Path(__file__) / "config"
)

candidate_paths = (dir / "config.yaml" for dir in config_locations)
config_paths = (path for path in candidate_paths if path.exists())
files_values = [yaml.load(str(path)) for path in config_paths]

env_settings = [
    ("samples", nint(os.environ.get("SIM_SAMPLES", None))),
    ("stake", nint(os.environ.get("SIM_STAKE", None))),
    ("rounds", nint(os.environ.get("SIM_ROUNDS", None))),
]

env_values = {
    k: v
    for k, v in env_settings if v is not None
}

defaults = argparse.Namespace(
    **ChainMap(
        env_values,  # Checks here first
        *files_values  # All the files, in order
    )
)
