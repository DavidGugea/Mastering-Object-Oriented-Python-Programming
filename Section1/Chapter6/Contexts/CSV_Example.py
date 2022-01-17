from pathlib import Path
from typing import Iterator
import gzip
import csv

source_path = Path.cwd()
target_path = Path.cwd()

with target_path.open("w", newline='') as target:
    wtr = csv.writer(target)
    with gzip.open(source_path) as source:
        line_iter = (b.decode() for b in source)
        row_iter = Counter(format_1_pat.match(line) for line in line_iter)
        non_empty_rows: Iterator[Match] = filter(None, row_iter)
        wtr.writerows(m.groups() for m in non_empty_rows)
