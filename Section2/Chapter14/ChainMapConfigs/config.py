from pathlib import Path
import typing
from typing import Any, Dict
from collections import ChainMap

config_name = "config.py"
config_locations = (
    Path.cwd(),
    Path.home(),
    Path("/etc/app"),
    Path(__file__)
)

candidates = (dir / config_name for dir in config_locations)
config_paths = (path for path in candidates if path.exists())

cm_config: typing.ChainMap[str, Any] = ChainMap()
for path in config_paths:
    config_layer: Dict[str, Any] = {}
    source_code = path.read_text()
    exec(source_code, globals(), config_layer)
    cm_config.maps.append(config_layer)

simulate(config.table, config.player, config.outputfile, config.samples)