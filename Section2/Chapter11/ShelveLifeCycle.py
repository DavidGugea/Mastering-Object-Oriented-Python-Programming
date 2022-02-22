import shelve
from contextlib import closing
from pathlib import Path

db_path = Path.cwd() / "save" / "directory"

with closing(shelve.open(str(db_path))) as shelf:
    process(shelf)