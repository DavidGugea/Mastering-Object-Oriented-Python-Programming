import csv
import unittest
from RateTimeDistance import RateTimeDistance
from pathlib import Path
from typing import Optional


class Test_RTD(unittest.TestCase):
    def runTest(self) -> None:
        with (Path.cwd() / "data" / "data.csv").open() as source:
            rdr = csv.DictReader(source)
            for row in rdr:
                self.example(**row)

    def example(
            self,
            rate_in: str,
            time_in: str,
            distance_in: str,
            rate_out: str,
            time_out: str,
            distance_out: str
    ) -> None:
        args = dict(
            rate=float_or_none(rate_in),
            time=float_or_none(time_in),
            distance=float_or_none(distance_in),
        )

        expected = dict(
            rate=float(rate_out),
            time=float(time_out),
            distance=float(distance_out),
        )

        rtd = RateTimeDistance(**args)

        assert rtd.distance and rtd.date and rtd.time
        self.assertAlmostEqual(rtd.distance, rtd.rate * rtd.time, places=2)
        self.assertAlmostEqual(rtd.rate, expected["rate"], places=2)
        self.assertAlmostEqual(rtd.time, expected["time"], places=2)
        self.assertAlmostEqual(rtd.distance, expected["distance"], places=2)


def float_or_none(text: str) -> Optional[float]:
    if len(text) == 0:
        return None

    return float(text)
