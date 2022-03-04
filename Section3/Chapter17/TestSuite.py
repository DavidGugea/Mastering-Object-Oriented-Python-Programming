from TestCard import TestCard
from TestAceCard import TestAceCard
import unittest


def suite() -> unittest.TestSuite:
    s = unittest.TestSuite()

    load_from = unittest.defaultTestLoader.loadTestsFromTestCase
    s.addTest(load_from(TestCard))
    s.addTest(load_from(TestAceCard))

    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())
