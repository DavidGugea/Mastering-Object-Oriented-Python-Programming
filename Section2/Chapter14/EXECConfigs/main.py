from typing import Dict, Any
from types import SimpleNamespace


code = compile(open("setup.py", "r").read(), "stringio", "exec")
assignments: Dict[str, Any] = dict()
exec(code, globals(), assignments)
config = SimpleNamespace(**assignments)

simulate(config.table, config.player, config.outputfile, config.samples)